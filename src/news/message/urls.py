from django.urls import path
from message import views

app_name = 'message'

urlpatterns = [
    path('search_user/', views.search_user, name='search_user'),
    path('chats/', views.ChatListView.as_view(), name='chats'),
    path('chats/<slug:username>//', views.DialogView.as_view(), name='dialog'),
]