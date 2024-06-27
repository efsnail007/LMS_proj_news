from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, View
from .models import Tags, Item, Addition, Comment, Feedback
from .forms import NewsCreationForm, NewCommentForm, FeedbackForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class NewsCreationView(CreateView):
    model = Item
    form_class = NewsCreationForm
    template_name = 'item/create.html'
    success_url = reverse_lazy('item:item_list')  

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

    # def test_func(self):
    #     post = self.get_object()
    #     if self.request.user == post.author:
    #         return True
    #     else:
    #         return False
    

class ItemDetailView(View):
    model = Item
    pk_url_kwarg = 'item_id'
    template_name = 'item/item_detail.html'
    # form_class = NewCommentForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        
        stuff = get_object_or_404(Item, id=self.kwargs['item_id'])
        
        # liked = False
        # if stuff.like.filter(id=self.request.user.id).exists():
        #     liked = True
        #
        # context["total_likes"] = total_likes
        # context["liked"] = liked

        return context


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    form_class = NewsCreationForm
    template_name = 'item/item_update.html'
    pk_url_kwarg = 'item_id'
    success_url = reverse_lazy('item:item_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    pk_url_kwarg = 'item_id'
    success_url = reverse_lazy('item:item_list')
    template_name = 'item/item_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class CommentCreateView(LoginRequiredMixin, View):

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


class FeedbackView(LoginRequiredMixin, CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'item/feedback.html'
    
    success_url = reverse_lazy('item:item_list') 
