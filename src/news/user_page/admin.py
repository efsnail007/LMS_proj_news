from django.contrib import admin
from .models  import Profile, Subscriptions, MarkedRecords

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'photo', 'user_tags')

    def user_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ['subscriber']
    # inlines = [SubscriptionInline]

@admin.register(MarkedRecords)
class MarkedRecordsAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'mark', 'text')
