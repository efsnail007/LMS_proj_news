from django.urls import path
from registration import views

app_name = 'registration'

urlpatterns = [
    path('', views.AuthView.as_view(), name='auth'),
    path('add/', views.RegView.as_view(), name='reg'),
    path('main/', views.StartView.as_view(), name='main'),
]