from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordResetForm
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

class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg border-3 rounded-0 field-style'
