from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, View
from .models import Tags, Item, Addition, Feedback
from user_page.models import Profile, MarkedRecords
from .forms import NewsCreationForm, FeedbackForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
import mimetypes

class NewsCreationView(CreateView):
    model = Item
    form_class = NewsCreationForm
    template_name = 'item/create.html'
    success_url = reverse_lazy('item:item_detail')  # потом заменить на ленту

    def form_valid(self, form):
        files = form.cleaned_data["files"]
        form.instance.author = get_object_or_404(User, username=self.request.user.username)
        for file in files:
            Addition.objects.create(item=form.save(), file=file)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('registration:auth')
        return super().dispatch(request, *args, **kwargs)
    

class ItemDetailView(View):
    model = Item
    template_name = 'item/item_detail.html'
    # form_class = NewCommentForm

    def __get_addition(self, item):
        type_and_file = {}
        addition = Addition.objects.filter(item_id=item.id)
        for file in addition:
            mimetype, _ = mimetypes.guess_type(str(file))
            type_and_file[str(file)] = mimetype.split('/')[0]
        return type_and_file

    def post(self, request, *args, **kwargs):
        form_name = request.POST.get('form_name')
        print(form_name)
        if form_name == 'like-form':
            record = MarkedRecords.objects.filter(item_id=self.kwargs['item_id'], mark='Like', user=Profile.objects.get(user_id=request.user.id)).exists()
            if not record:
                MarkedRecords.objects.create(item=Item.objects.get(id=self.kwargs['item_id']), user=Profile.objects.get(user_id=request.user.id), mark='Like')
                return JsonResponse({'is_liked': True})
            MarkedRecords.objects.get(item_id=self.kwargs['item_id'], mark='Like', user=Profile.objects.get(user_id=request.user.id)).delete()
            return JsonResponse({'is_liked': False})
        return redirect('item:item_detail', item_id=self.kwargs['item_id'])

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(Item, id=self.kwargs['item_id'])
        profile = Profile.objects.get(user_id=item.author.id)
        likes_count = MarkedRecords.objects.filter(item=self.kwargs['item_id'], mark='Like').count()
        return render(request, self.template_name, {'item': item, 'profile': profile, 'addition': self.__get_addition(item), 'likes_count': likes_count})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('registration:auth')
        return super().dispatch(request, *args, **kwargs)


class ItemUpdateView(UpdateView):
    model = Item
    form_class = NewsCreationForm
    template_name = 'item/item_update.html'
    pk_url_kwarg = 'item_id'
    success_url = reverse_lazy('item:item_detail')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('registration:auth')
        return super().dispatch(request, *args, **kwargs)

class ItemDeleteView(DeleteView):
    model = Item
    pk_url_kwarg = 'item_id'
    success_url = reverse_lazy('registration:main') # заменить на news-feed
    template_name = 'item/item_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != Item.objects.get(id=self.kwargs[self.pk_url_kwarg]).author.id:
            return redirect('item:item_detail', item_id=self.kwargs[self.pk_url_kwarg])
        return super().dispatch(request, *args, **kwargs)

class CommentCreateView(View):

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        current_user = request.user
        item_id = self.kwargs['item_id']
        comment_post = Item.objects.filter(id=item_id).first()
        new_comment = Comment(
            author=current_user,
            item=comment_post,
            text=request.POST['text'],
        )
        new_comment.save()
        return redirect("item:item_detail", item_id=item_id)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('registration:auth')
        return super().dispatch(request, *args, **kwargs)

class FeedbackView(View):
    model = Feedback
    template_name = 'item/feedback.html'

    def post(self, request, *args, **kwargs):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            text = form.data['feedback_text']
            Feedback.objects.create(text_feedback=text, user=request.user, item=Item.objects.get(id=self.kwargs['item_id']))
            return redirect('item:item_detail', item_id=self.kwargs['item_id'])
        return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'item_id': self.kwargs['item_id'], 'form': FeedbackForm()})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('registration:auth')
        return super().dispatch(request, *args, **kwargs)
