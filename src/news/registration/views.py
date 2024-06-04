from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from registration.forms import RegistrationForm, LoginForm

class RegView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'auth_and_reg/reg.html'
    success_url = reverse_lazy('auth_and_reg:auth')


class AuthView(LoginView):
    authentication_form = LoginForm
    template_name = 'auth_and_reg/auth.html'
    redirect_authenticated_user = reverse_lazy('auth_and_reg:start')
