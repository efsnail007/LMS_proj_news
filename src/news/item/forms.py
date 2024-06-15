from django import forms
from .models import Tags, Item, Addition

class NewsCreationForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['text', 'tags']
        labels = {'text': 'Текст'}
        # widgets = {'tags': forms.ModelMultipleChoiceField(queryset=Tags.objects.all())}
    tags = forms.ModelMultipleChoiceField(queryset=Tags.objects.all(), widget=forms.CheckboxSelectMultiple, label='Теги', to_field_name='name')
