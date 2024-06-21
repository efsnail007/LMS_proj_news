from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from registration.forms import RegistrationForm, LoginForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import User
from user_page.models import Profile, Subscriptions

class MainView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/main.html')


class RegView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'registration/reg.html'
    success_url = reverse_lazy('registration:auth')

    def form_valid(self, form):
        form.instance.password = make_password(form.cleaned_data['password'])
        Profile.objects.create(user=form.save())
        Subscriptions.objects.create(subscriber=form.save())
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('registration:main')
        return super().dispatch(request, *args, **kwargs)

class AuthView(LoginView):
    authentication_form = LoginForm
    template_name = 'registration/auth.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('registration:main')
