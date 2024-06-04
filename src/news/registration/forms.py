from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        labels = {'username': 'Логин', 'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Почта', 'password': 'Пароль'}
        help_texts = {'username': ''}
        required = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {'password': forms.PasswordInput}

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cd['password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, label='Логин', widget=forms.TextInput)
    password = forms.CharField(max_length=128, label='Пароль', widget=forms.PasswordInput)

    class Meta:
        fields = ['username', 'password']
