from django.db import models
from django.conf import settings
from item.models import Tags


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    tags = models.ManyToManyField(Tags)


class Subscriptions(models.Model):
    subscriber = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscription_profiles = models.ManyToManyField(Profile)
