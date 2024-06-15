from django.shortcuts import render
from django.views.generic import CreateView
from .models import Tags, Item, Addition
from .forms import NewsCreationForm

# Create your views here.

class NewsCreationView(CreateView):
    model = Item
    form_class = NewsCreationForm
    template_name = 'item/create.html'
