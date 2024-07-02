from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, View
from .models import Tags, Item, Addition, Feedback
from user_page.models import Profile, MarkedRecords
from .forms import NewsCreationForm, FeedbackForm, NewCommentForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
import mimetypes


def get_addition(item):
    type_and_file = {}
    addition = Addition.objects.filter(item_id=item.id)
    for file in addition:
        mimetype, _ = mimetypes.guess_type(str(file))
        type_and_file[str(file)] = [mimetype.split('/')[0], file.id]
    return type_and_file


class NewsCreationView(CreateView):
    model = Item
    form_class = NewsCreationForm
    template_name = 'item/create.html'

    def form_valid(self, form):
        files = form.cleaned_data["files"]
        form.instance.author = get_object_or_404(User, username=self.request.user.username)
        for i in range(len(files)):
            if i > 8:
                break
            Addition.objects.create(item=form.save(), file=files[i])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('registration:main') # потом заменить на ленту

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('registration:auth')
        return super().dispatch(request, *args, **kwargs)
    

class ItemDetailView(View):
    model = Item
    template_name = 'item/item_detail.html'

    def post(self, request, *args, **kwargs):
        form_name = request.POST.get('form_name')
        profile = Profile.objects.get(user_id=request.user.id)
        if form_name == 'like-form':
            record = MarkedRecords.objects.filter(item_id=self.kwargs['item_id'], mark='Like', user=profile).exists()
            if not record:
                MarkedRecords.objects.create(item=Item.objects.get(id=self.kwargs['item_id']), user=profile, mark='Like')
                return JsonResponse({'is_liked': True})
            MarkedRecords.objects.get(item_id=self.kwargs['item_id'], mark='Like', user=profile).delete()
            return JsonResponse({'is_liked': False})
        elif form_name == 'comment-form':
            form = NewCommentForm(request.POST)
            if form.is_valid():
                text = form.data['comment_text']
                MarkedRecords.objects.create(item=Item.objects.get(id=self.kwargs['item_id']), user=profile, mark='Comment', text=text)
                return JsonResponse({'text': text, 'username': request.user.username, 'photo': profile.photo.url})
        elif form_name == 'repost-form':
            record = MarkedRecords.objects.filter(item_id=self.kwargs['item_id'], mark='Repost', user=profile).exists()
            if not record:
                MarkedRecords.objects.create(item=Item.objects.get(id=self.kwargs['item_id']), user=profile, mark='Repost')
                return JsonResponse({'is_reposted': True})

        return redirect('item:item_detail', item_id=self.kwargs['item_id'])

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(Item, id=self.kwargs['item_id'])
        profile = Profile.objects.get(user_id=item.author.id)
        likes_count = MarkedRecords.objects.filter(item=self.kwargs['item_id'], mark='Like').count()
        all_comments = MarkedRecords.objects.filter(item=self.kwargs['item_id'], mark='Comment')[::-1]
        reposts_count = MarkedRecords.objects.filter(item=self.kwargs['item_id'], mark='Repost').count()
        return render(request, self.template_name, {'item': item, 'profile': profile,
        'addition': get_addition(item), 'likes_count': likes_count, 'comment_form': NewCommentForm(), 'all_comments': all_comments, 'reposts_count': reposts_count})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('registration:auth')
        return super().dispatch(request, *args, **kwargs)


class ItemUpdateView(UpdateView):
    model = Item
    form_class = NewsCreationForm
    template_name = 'item/item_update.html'
    pk_url_kwarg = 'item_id'

    def get_context_data(self, *kwargs):
        context = super().get_context_data(*kwargs)
        item_files = get_addition(Item.objects.get(id=self.kwargs[self.pk_url_kwarg]))
        context['item_files'] = item_files
        return context

    def post(self, request, *args, **kwargs):
        form = NewsCreationForm(request.POST)
        if form.is_valid():
            for add in Addition.objects.filter(item_id=self.kwargs[self.pk_url_kwarg]):
                if request.POST.get('photo-clear-' + str(add.id)) == 'on':
                    Addition.objects.filter(id=add.id).delete()
            files = request.FILES.getlist('files')
            adds_count = Addition.objects.filter(item_id=self.kwargs[self.pk_url_kwarg]).count()
            for i in range(len(files)):
                if i + adds_count > 8:
                    break
                Addition.objects.create(item_id=self.kwargs[self.pk_url_kwarg], file=files[i])
            itm = Item.objects.filter(id=self.kwargs[self.pk_url_kwarg])
            itm.update(text=form.cleaned_data['text'])
            itm.first().tags.clear()
            for tag in request.POST.getlist('tags'):
                itm.first().tags.add(Tags.objects.get(name=tag))
            return redirect('item:item_detail', item_id=self.kwargs[self.pk_url_kwarg])
        return render(request, self.template_name, {'form': form})

    def get_success_url(self):
        return reverse_lazy('item:item_detail', args=[self.kwargs[self.pk_url_kwarg]])

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != Item.objects.get(id=self.kwargs[self.pk_url_kwarg]).author.id:
            return redirect('item:item_detail', item_id=self.kwargs[self.pk_url_kwarg])
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
