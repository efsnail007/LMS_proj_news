from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    error_messages = {
        'password_mismatch': 'Пароли не равны',
        'password_notvalid': "Пароль должен состоять из 8 символов и содержать как минимум 1 специальный символ и 1 заглавную букву.",
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.required:
            self.fields[field].required = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        labels = {'username': 'Логин', 'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Почта', 'password': 'Пароль'}
        help_texts = {'username': ''}
        required = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {'password': forms.PasswordInput, 'email': forms.EmailInput}

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
            regex = re.compile('((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%]).{8,30})')
            if regex.search(password1) == None:
                    raise forms.ValidationError(
                    self.error_messages['password_notvalid'],
                    code='password_notvalid',
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
