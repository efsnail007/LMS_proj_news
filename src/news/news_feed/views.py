from django.shortcuts import render
from django.views import View
from item.models import Item, Addition, Tags
from user_page.models import Profile
from django.http import JsonResponse
import mimetypes
from datetime import datetime
import locale

# Create your views here.

class NewsFeedView(View):
    template_name = "news_feed/main.html"
    __num_of_items = 10

    def __get_addition(self, item):
        type_and_file = {}
        addition = Addition.objects.filter(item_id=item.id)
        for file in addition:
            mimetype, _ = mimetypes.guess_type(str(file))
            type_and_file[str(file)] = mimetype.split('/')[0]
        return type_and_file

    def get(self, request, *args, **kwargs):
        items = Item.objects.all().order_by('-created_at')
        page = int(request.GET.get('page', 1))
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
            items_for_unauthenticated = [{'item': {
                'username': item.author.username,
                'text': item.text,
                'tags': [str(tag) for tag in item.tags.all()],
                'created_at': datetime.strftime(item.created_at, "%d %B %Y %H:%M"),
            }, 'profile': str(Profile.objects.get(user_id=item.author.id).photo.url) if Profile.objects.get(user_id=item.author.id).photo else None,
            'addition': self.__get_addition(item)}
                                         for item in items[page*self.__num_of_items:(page+1) * self.__num_of_items]]
            return JsonResponse({'items_for_unauthenticated': items_for_unauthenticated})
        items_for_unauthenticated = [[item, Profile.objects.get(user_id=item.author.id), self.__get_addition(item)] for
                                     item in items[:self.__num_of_items]]
        return render(request, self.template_name, {'items_for_unauthenticated': items_for_unauthenticated})
