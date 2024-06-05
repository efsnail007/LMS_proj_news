from django.urls import path
from reset_password import views
from django.contrib.auth import views as reset_views

app_name = 'reset_password'

urlpatterns = [
    path('', reset_views.PasswordResetView.as_view(), name='reset_password'),
]