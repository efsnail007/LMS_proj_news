from django.urls import path
from news_feed import views

app_name = 'news_feed'

urlpatterns = [
    path('', views.NewsFeedView.as_view(), name='news-feed'),
]