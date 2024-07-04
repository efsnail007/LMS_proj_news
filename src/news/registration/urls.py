from django.urls import path
from registration import views

app_name = 'registration'

urlpatterns = [
    path('', views.AuthView.as_view(), name='auth'),
    path('add/', views.RegView.as_view(), name='add'),
    path('logout/', views.logout_view, name='logout'),
]