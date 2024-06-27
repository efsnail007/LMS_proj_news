from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
import re


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    er_mes = {
        'password_mismatch': 'Введённые пароли не равны',
        'username_first_symbol': 'Первый символ логина должен быть латинской буквой или нижним подчёркиванием',
        'username_length': 'Длина логина должна быть равна от 3 до 15 символов',
        'username_symbols': 'Логин должен в себя включать только латинские буквы, цифры или символы нижнего подчёркивания',
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.required:
            self.fields[field].required = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg border-3 rounded-0 field-style'


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        labels = {'username': 'Логин', 'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Почта', 'password': 'Пароль'}
        help_texts = {'username': ''}
        required = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {'password': forms.PasswordInput, 'email': forms.EmailInput}

    def clean_username(self):
        username_value = self.cleaned_data.get('username')
        match = re.match(r"^[a-zA-Z_][a-zA-Z0-9_]{3,15}$", username_value)
        if bool(match):
            return username_value
        if len(username_value) > 16 or len(username_value) < 3:
            raise forms.ValidationError(self.er_mes['username_length'])
        match = re.match(r"^[a-zA-Z_]$", username_value[0])
        if not bool(match):
            raise forms.ValidationError(self.er_mes['username_first_symbol'])
        raise forms.ValidationError(self.er_mes['username_symbols'])


    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.er_mes['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(str(password2))
        return password2

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким адресом электронной почты уже зарегистрирован.")
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, label='Логин', widget=forms.TextInput)
    password = forms.CharField(max_length=128, label='Пароль', widget=forms.PasswordInput)

    class Meta:
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg border-3 rounded-0 field-style'
