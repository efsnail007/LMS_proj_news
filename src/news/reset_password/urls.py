from django.urls import path
from reset_password import views, forms
from django.contrib.auth import views as reset_views
from django.urls import reverse_lazy

app_name = 'reset_password'

urlpatterns = [
    path('', views.CustomPasswordResetView.as_view(form_class=forms.UserPasswordResetForm), name='reset_password'),
    path('done/', reset_views.PasswordResetDoneView.as_view(template_name='reset_password/reset_password_done.html'), name='reset_password_done'),
    path('<uidb64>/<token>/', reset_views.PasswordResetConfirmView.as_view(template_name='reset_password/set_password.html', form_class=forms.UserSetPasswordForm, success_url=reverse_lazy('reset_password:password_reset_complete')), name ='reset_password_confirm'),
    path('complete/', reset_views.PasswordResetCompleteView.as_view(template_name='reset_password/complete.html'), name='password_reset_complete'),
]