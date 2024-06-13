from django import forms
from .models import Profile

class UserPageEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
        labels = {'date_of_birth': 'Дата рождения', 'photo': 'Фото'}
        widgets = {'date_of_birth': forms.DateInput(format='%d.%m.%Y', )}
