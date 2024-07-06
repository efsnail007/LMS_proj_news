from django import forms
from .models import Item, Addition, Tags, Feedback

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'accept':'image/*,video/*', 'class': 'hidden-elem form-control border-3 rounded-0 field-style', 'id': 'id_photo'}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class NewsCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['class'] = 'form-control field-style border-3 rounded-0'

    class Meta:
        model = Item
        fields = ['text', 'files', 'tags']
        labels = {'text': 'Текст'}
    tags = forms.ModelMultipleChoiceField(queryset=Tags.objects.all(), widget=forms.CheckboxSelectMultiple, label='Теги', to_field_name='name')
    files = MultipleFileField(label='Файлы', required=False)


class NewCommentForm(forms.Form):
    comment_text = forms.CharField(label="Комментарий", widget=forms.Textarea(attrs={'class': 'form-control field-style border-3 rounded-0'}))


class FeedbackForm(forms.Form):
    feedback_text = forms.CharField(label='Жалоба', widget=forms.Textarea)
