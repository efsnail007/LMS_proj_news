from django.shortcuts import render
from django.views.generic import CreateView
from .models import Tags, Item, Addition
from .forms import NewsCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

# Create your views here.

class NewsCreationView(CreateView):
    model = Item
    form_class = NewsCreationForm
    template_name = 'item/create.html'
    success_url = reverse_lazy('registration:main')

    # def get_context_data(self, *kwargs):
    #     context = super().get_context_data(*kwargs)
    #     context['addition_form'] = AdditionCreationForm()
    #     return context

    def form_valid(self, form):
        files = form.cleaned_data["files"]
        form.instance.author = get_object_or_404(User, username=self.request.user.username)
        for file in files:
            Addition.objects.create(item=form.save(), file=file)
        return super().form_valid(form)
