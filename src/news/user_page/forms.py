from django import forms
from .models import Profile
from item.models import Tags

class UserPageEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].required = False
        self.fields['date_of_birth'].widget.attrs['class'] = 'form-control border-3 rounded-0 field-style'

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo', 'tags']
        labels = {'date_of_birth': 'Дата рождения', 'photo': 'Загружаемое изображение'}
        widgets = {'date_of_birth': forms.DateInput(format='%d.%m.%Y', )}

    tags = forms.ModelMultipleChoiceField(queryset=Tags.objects.all(), widget=forms.CheckboxSelectMultiple, label='Любимые теги', to_field_name='name')
