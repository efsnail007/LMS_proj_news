from django.db import models
from django.conf import settings

class Tags(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    tags = models.ManyToManyField(Tags)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Addition(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    file = models.FileField(upload_to='news/%Y/%m/%d/')

    def __str__(self):
        return self.file.url


class Feedback(models.Model):
    text_feedback = models.TextField(default='Жалоба')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='feedback')

    def __str__(self):
        return f'{self.user}, {self.item}'

    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'