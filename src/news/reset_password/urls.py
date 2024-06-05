from django.urls import path
from reset_password import views
from django.contrib.auth import views as reset_views

app_name = 'reset_password'

urlpatterns = [
    path('', views.CustomPasswordResetView.as_view(), name='reset_password'),
    path('done/', reset_views.PasswordResetDoneView.as_view(), name='reset_password_done'),
    path('<uidb64>/<token>/', reset_views.PasswordResetConfirmView.as_view(), name ='reset_password_confirm'),
    path('complete/', reset_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]