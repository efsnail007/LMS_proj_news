from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from item.models import Item, Addition, Tags
from user_page.models import Profile
import mimetypes

# Create your views here.

class NewsFeedView(View):
    template_name = "news_feed/main.html"

    def __get_addition(self, item):
        type_and_file = {}
        addition = Addition.objects.filter(item_id=item.id)
        for file in addition:
            mimetype, _ = mimetypes.guess_type(str(file))
            type_and_file[str(file)] = mimetype.split('/')[0]
        return type_and_file

    def get(self, request, *args, **kwargs):
        items = Item.objects.all()
        items_for_unauthenticated = [[item, Profile.objects.get(user_id=item.author.id), self.__get_addition(item)] for item in items]
        return render(request, self.template_name, {'items_for_unauthenticated': items_for_unauthenticated})
