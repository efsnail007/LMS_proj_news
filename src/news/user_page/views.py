from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView
from .models import Profile
from .forms import UserPageEditForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User

# Create your views here.

class UserPageView(View):
    template_name = 'user_page/user_page.html'

    def get(self, request, *args, **kwargs):
        record = Profile.objects.get(user_id=User.objects.get(username=self.kwargs['username']).id)
        return render(request, self.template_name, {'record': record})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('registration:auth')
        return super().dispatch(request, *args, **kwargs)


class UserPageViewEdit(UpdateView):
    template_name = 'user_page/user_page_edit.html'
    model = Profile
    form_class = UserPageEditForm

    def get_object(self, queryset=None):
        return Profile.objects.get(user_id=User.objects.get(username=self.kwargs['username']).id)

    def get_success_url(self):
        return reverse_lazy('user_page:user-page', args=[self.kwargs['username']])

    def dispatch(self, request, *args, **kwargs):
        if self.kwargs['username'] != request.user.username:
            return redirect('user_page:user-page', self.kwargs['username'])
        return super().dispatch(request, *args, **kwargs)

