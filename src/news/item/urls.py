from django.urls import path
from item import views

app_name = 'item'

urlpatterns = [
    path('add/', views.NewsCreationView.as_view(), name='item-add'),
]