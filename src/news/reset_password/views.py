from django.shortcuts import render
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import redirect
from django.urls import reverse_lazy

# Create your views here.

class CustomPasswordResetView(PasswordResetView):
    template_name = 'reset_password/reset_password.html'
    email_template_name = 'reset_password/password_reset_form.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('registration:main')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('reset_password:reset_password_done')
