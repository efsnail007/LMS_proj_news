from django.contrib.auth.forms import SetPasswordForm
from django import forms


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput,
        strip=False,
    )
    new_password2 = forms.CharField(
        label='Повторите новый пароль',
        strip=False,
        widget=forms.PasswordInput,
    )
