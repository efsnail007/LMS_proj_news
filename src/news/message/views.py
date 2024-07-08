from django.shortcuts import render, redirect, reverse
from .models import Message
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, View
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from user_page.models import Profile
from .forms import MessageForm
from user_page.models import Profile


def search_user(request):
    if not request.user.is_authenticated:
        return redirect('registration:auth')
    if request.method == 'POST':
        search = request.POST['search']
        searched = [Profile.objects.get(user=user) for user in User.objects.filter(username__icontains=search, is_superuser=False)]
        return render(request, 'messages/search_user.html', {'search': search, 'searched': searched})
    searched = Profile.objects.all()
    return render(request, 'messages/search_user.html', {'searched': searched})
