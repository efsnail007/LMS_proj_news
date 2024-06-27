from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, View
from .models import Tags, Item, Addition, Feedback
from user_page.models import Profile
from .forms import NewsCreationForm, FeedbackForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
    pk_url_kwarg = 'item_id'
    template_name = 'item/item_detail.html'
    # form_class = NewCommentForm

    def __get_addition(self, item):
        type_and_file = {}
        addition = Addition.objects.filter(item_id=item.id)
        for file in addition:
            mimetype, _ = mimetypes.guess_type(str(file))
            type_and_file[str(file)] = mimetype.split('/')[0]
        return type_and_file

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(Item, id=self.kwargs['item_id'])
        profile = Profile.objects.get(user_id=item.author.id)
        return render(request, self.template_name, {'item': item, 'profile': profile, 'addition': self.__get_addition(item)})

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

class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    pk_url_kwarg = 'item_id'
    success_url = reverse_lazy('registration:main') # заменить на news-feed
    template_name = 'item/item_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

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


def LikeView(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    liked = False
    if item.like.filter(id=request.user.id).exists():
        item.like.remove(request.user)
        liked = False
    else:
        item.like.add(request.user)
        liked = True

    return redirect("item:item_detail", item_id=item_id)


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
