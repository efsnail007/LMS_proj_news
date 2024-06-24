from django.shortcuts import render
from django.views import View

# Create your views here.

class NewsFeedView(View):
    template_name = "news_feed/main.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
