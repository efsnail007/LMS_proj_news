from django.urls import path
from registration import views
from django.contrib.auth.views import LogoutView

app_name = 'registration'

urlpatterns = [
    path('', views.AuthView.as_view(), name='auth'),
    path('add/', views.RegView.as_view(), name='add'),
    path('main/', views.MainView.as_view(), name='main'),
    path('logout/', LogoutView.as_view(template_name='registration/main.html'), name='logout'),
]