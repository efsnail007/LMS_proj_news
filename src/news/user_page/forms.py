from django import forms
from .models import Profile
from item.models import Tags

class UserPageEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
        labels = {'date_of_birth': 'Дата рождения', 'photo': 'Изображение'}
        widgets = {'date_of_birth': forms.DateInput(format='%d.%m.%Y', )}

    tags = forms.ModelMultipleChoiceField(queryset=Tags.objects.all(), widget=forms.CheckboxSelectMultiple, label='Любимые теги', to_field_name='name')
