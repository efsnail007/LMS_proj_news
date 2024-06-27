from django import forms
from .models import Item, Addition, Comment, Tags, Feedback

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'accept':'image/*,video/*'}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class NewsCreationForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'text', 'tags']
        labels = {'title': 'Название', 'text': 'Текст'}
    tags = forms.ModelMultipleChoiceField(queryset=Tags.objects.all(), widget=forms.CheckboxSelectMultiple, label='Теги', to_field_name='name')
    files = MultipleFileField(label='Файлы', required=False)


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
        labels =  {'text': 'Текст', 'author': 'Автор комментария'}
    

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['user', 'email', 'text_feedback', 'item']
        labels =  {'text_feedback': 'Текст', 'user': 'Пользователь', 'email': 'Почта', 'item': 'Новость'}