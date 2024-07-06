from django.db import models
from django.conf import settings
from datetime import datetime, timedelta

# Create your models here.

class Tags(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Теги'
        verbose_name_plural = 'Теги'


class Item(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    tags = models.ManyToManyField(Tags)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'


class Addition(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    file = models.FileField(upload_to='news/%Y/%m/%d/')

    def __str__(self):
        return self.file.url

    class Meta:
        verbose_name = 'Дополнительная информация к посту'
        verbose_name_plural = 'Дополнительная информация к посту'


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