from django.shortcuts import render, redirect, reverse
from .models import Message
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, View
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from user_page.models import Profile
from .forms import MessageForm


def search_user(request):

    if request.method == 'POST':
        search = request.POST['search']
        searched = User.objects.filter(username__icontains = search)
        return render(request, 'messages/search_user.html', {'search': search, 'searched': searched})
    else:
        return render(request, 'messages/search_user.html', {})




class ChatListView(ListView):
    model = Message
    template_name = 'messages/chat.html'
    
    def get(self, request):
        chats = (Message.objects.filter(sender=request.user) | Message.objects.filter(reciever=request.user))
        return render(request, self.template_name, {'user_profile': request.user, 'chats': chats})

class CreateMessageView(CreateView):
    model = Message
    template_name = 'messages/create_message.html'

    def get(self, request):
        chats = (Message.objects.filter(sender=request.user) | Message.objects.filter(reciever=request.user))
        reciever_user = User.objects.get(username = reciever_name)
        
        return render(request, self.template_name, {'user_profile': request.user, 'chats': chats})



class DialogView(View):
    model = Message
    template_name = 'messages/dialog.html'

    def get(self, request, username):
        companion = User.objects.get(username = username)
        sender = Message.objects.filter(sender = request.user)
        messages = (Message.objects.filter(sender = request.user, reciever = companion) | Message.objects.filter(reciever = request.user, sender = companion)).order_by("-created_at")
        messages2 = (Message.objects.filter(sender = request.user, reciever = companion) | Message.objects.filter(reciever = request.user, sender = companion)).order_by("-created_at")
        not_readed_messages = Message.objects.filter(reciever = request.user, sender = companion, is_readed = False)
        for message in not_readed_messages:
            message.is_readed = True
            message.save()
        context = {'sort_messages':messages[::-1], 'companion': companion, 'messages2': messages2}
        return render(request, 'messages/dialog.html', context)
