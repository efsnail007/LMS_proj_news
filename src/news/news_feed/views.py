from django.shortcuts import render
from django.views import View
from item.models import Item, Addition, Tags
from user_page.models import Profile, Subscriptions
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

    def __get_items(self, items, page):
        return [{'item': {
            'username': item.author.username,
            'text': item.text,
            'tags': [str(tag) for tag in item.tags.all()],
            'created_at': datetime.strftime(item.created_at, "%d %B %Y г. %-H:%M"),
        }, 'profile': str(Profile.objects.get(user_id=item.author.id).photo.url) if Profile.objects.get(
            user_id=item.author.id).photo else None,
            'addition': self.__get_addition(item)}
            for item in items[page * self.__num_of_items:(page + 1) * self.__num_of_items]]

    def __set_items(self, request, tags):
        subscriptions = None
        if request.user.is_authenticated:
            subscriptions = [Profile.objects.get(id=item.id).user.id for item in
                             Subscriptions.objects.get(subscriber=request.user.id).subscription_profiles.all()]
        filter_ar = []
        for tag in tags:
            if str(tag) in request.session.get('filter', []):
                filter_ar.append(tag)
        if len(filter_ar) > 0:
            if 'Подписки' in request.session.get('filter', []) and request.user.is_authenticated:
                return Item.objects.filter(author__in=subscriptions, tags__in=filter_ar).order_by(
                    '-created_at').distinct(), filter_ar.append('Подписки')
            return Item.objects.filter(tags__in=filter_ar).order_by('-created_at').distinct(), filter_ar
        else:
            if 'Подписки' in request.session.get('filter', []) and request.user.is_authenticated:
                return Item.objects.filter(author__in=subscriptions).order_by('-created_at').distinct(), filter_ar.append('Подписки')
        return Item.objects.all().order_by('-created_at'), []


    def get(self, request, *args, **kwargs):
        tags = Tags.objects.all()
        page = int(request.GET.get('page', 1))
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            action = request.GET.get('action')
            filter = request.GET.get('filter').split()
            request.session['filter'] = filter
            items, _ = self.__set_items(request, tags)
            locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
            if action == 'feed':
                items_for_answer = self.__get_items(items, page)
                return JsonResponse({'all_data': items_for_answer, 'page': page})
        items, context_filter_session = self.__set_items(request, tags)
        items_for_answer = [[item, Profile.objects.get(user_id=item.author.id), self.__get_addition(item)] for
                                     item in items[:self.__num_of_items]]
        if not request.user.is_authenticated:
            return render(request, self.template_name, {'items': items_for_answer, 'tags': tags, 'filter_session': context_filter_session})
        return render(request, self.template_name,
                      {'items': items_for_answer, 'tags': tags, 'filter_session': context_filter_session,
                       'tags_for_you': [str(tag) for tag in Profile.objects.get(user_id=request.user.id).tags.all()]})