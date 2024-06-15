from django.db import models
from django.conf import settings

# Create your models here.

class Tags(models.Model):
    name = models.CharField(max_length=100)


class Item(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    tags = models.ManyToManyField(Tags)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Addition(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    file = models.FileField(upload_to='news/%Y/%m/%d/')
