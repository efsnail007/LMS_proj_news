from django.urls import path
from message import views

app_name = 'message'

urlpatterns = [
    path('', views.search_user, name='search_user'),
]