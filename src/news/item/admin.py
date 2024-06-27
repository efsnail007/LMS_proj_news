from django.contrib import admin
from .models  import Item, Tags, Feedback

# @admin.register(Item)
# class ItemAdmin(admin.ModelAdmin):
#     list_display = ('author')
#
# @admin.register(Tags)
# class TagsAdmin(admin.ModelAdmin):
#     pass
#
# @admin.register(Feedback)
# class FeedbackAdmin(admin.ModelAdmin):
#     list_display = ('item', 'user', 'email')