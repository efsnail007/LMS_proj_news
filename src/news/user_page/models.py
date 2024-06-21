from django.db import models
from django.conf import settings
from item.models import Tags, Item


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    tags = models.ManyToManyField(Tags)


class Subscriptions(models.Model):
    subscriber = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscription_profiles = models.ManyToManyField(Profile)


class MarkedRecords(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    mark = models.CharField(max_length=50, choices=[('Like', 'Лайк'), ('Repost', 'Репост'), ('Comment', 'Комментарий')])
    text = models.TextField(blank=True, null=True)
