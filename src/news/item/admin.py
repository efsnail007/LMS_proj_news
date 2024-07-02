from django.contrib import admin
from .models  import Item, Tags, Feedback, Addition

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'created_at', 'updated_at')

@admin.register(Addition)
class AdditionAdmin(admin.ModelAdmin):
    list_display = ('item', 'file')

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'created_at', 'text_feedback')