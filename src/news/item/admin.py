from django.contrib import admin
from .models  import Item, Comment, Tags, Feedback

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'item')

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    pass

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'email')