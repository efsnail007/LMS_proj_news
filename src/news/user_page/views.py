from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView
from .models import Profile, Subscriptions, MarkedRecords
from .forms import UserPageEditForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from item.models import Item, Addition
from datetime import datetime
import mimetypes

# Create your views here.

month_dict = {
    "January": "января",
    "February": "февраля",
    "March": "марта",
    "April": "апреля",
    "May": "мая",
    "June": "июня",
    "July": "июля",
    "August": "августа",
    "September": "сентября",
    "October": "октября",
    "November": "ноября",
    "December": "декабря"
}


def created_at_month(created_at):
    ar = created_at.split(' ')
    ar[1] = month_dict[ar[1]]
    return ' '.join(ar)


# просмотр страницы пользователя
class UserPageView(View):
    template_name = 'user_page/user_page.html'
    __num_of_items = 10

    def __get_addition(self, item):
        type_and_file = {}
        addition = Addition.objects.filter(item_id=item.id)
        for file in addition:
            mimetype, _ = mimetypes.guess_type(str(file))
            type_and_file[str(file)] = mimetype.split('/')[0]
        return type_and_file

    def __get_is_subscribed(self, request):
        record_subscription = Subscriptions.objects.get(subscriber_id=request.user.id)
        all_records = list(record_subscription.subscription_profiles.all())
        if len(all_records) > 0:
            for item in all_records:
                if str(item) == self.kwargs['username']:
                    return True
            return False
        return False

    def __get_items(self, request_username, items, page):
        return [{'item': {
            'id': item.id,
            'username': item.author.username,
            'text': item.text,
            'tags': [str(tag) for tag in item.tags.all()],
            'created_at': created_at_month(datetime.strftime(item.updated_at, "%-d %B %Y г. %-H:%M")),
            'is_repost': item.author.username != self.kwargs['username'] and request_username == self.kwargs['username'],
        }, 'profile': str(Profile.objects.get(user_id=item.author.id).photo.url) if Profile.objects.get(
            user_id=item.author.id).photo else None,
            'addition': self.__get_addition(item),}
            for item in items[page * self.__num_of_items:(page + 1) * self.__num_of_items]]

    def get(self, request, *args, **kwargs):
        page = int(request.GET.get('page', 1))
        reposts = [record.item for record in
                   MarkedRecords.objects.filter(user=Profile.objects.get(user_id=User.objects.get(username=self.kwargs['username']).id),
                                                mark='Repost')]
        ids = [repost.id for repost in reposts]
        for item in Item.objects.filter(author=User.objects.get(username=self.kwargs['username'])):
            ids.append(item.id)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            repost = request.GET.get('repost', None)
            if repost:
                record = MarkedRecords.objects.get(user=Profile.objects.get(user_id=User.objects.get(username=self.kwargs['username']).id), item_id=int(repost), mark='Repost')
                record.delete()
                return JsonResponse({})

            action = request.GET.get('action')
            items = Item.objects.filter(id__in=ids).order_by('-created_at').distinct()

            if action == 'feed':
                items_for_answer = self.__get_items(request.user.username, items, page)
                return JsonResponse({'all_data': items_for_answer, 'page': page})

        record = Profile.objects.get(user_id=User.objects.get(username=self.kwargs['username']).id)
        items = Item.objects.filter(id__in=ids).order_by('-created_at').distinct()
        user_items = [[item, Profile.objects.get(user_id=item.author.id), self.__get_addition(item), item.author.username != self.kwargs['username'] and request.user.username == self.kwargs['username']] for
                            item in items[:self.__num_of_items]]
        return render(request, self.template_name, {'user_items': user_items,'record': record, 'is_subscribed': self.__get_is_subscribed(request)})

    def post(self, request, *args, **kwargs):
        form_name = request.POST.get('form_name')
        if form_name == 'subscribe-form':
            record_subscription = Subscriptions.objects.get(subscriber_id=request.user.id)
            flag = self.__get_is_subscribed(request)
            user_id = User.objects.get(username=self.kwargs['username']).id
            profile_item = Profile.objects.get(user_id=user_id)
            if not flag:
                record_subscription.subscription_profiles.add(profile_item)
                return JsonResponse({'success': True, 'text': 'Вы подписаны'})
            else:
                record_subscription.subscription_profiles.remove(profile_item)
                return JsonResponse({'success': True, 'text': 'Подписаться'})
        return redirect('user_page:user-page', username=self.kwargs['username'])

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('registration:auth')
        return super().dispatch(request, *args, **kwargs)


# редактирование страницы
class UserPageViewEdit(UpdateView):
    template_name = 'user_page/user_page_edit.html'
    model = Profile
    form_class = UserPageEditForm

    def get_object(self, queryset=None):
        return Profile.objects.get(user_id=User.objects.get(username=self.kwargs['username']).id)

    def get_success_url(self):
        return reverse_lazy('user_page:user-page', args=[self.kwargs['username']])

    def dispatch(self, request, *args, **kwargs):
        if self.kwargs['username'] != request.user.username:
            return redirect('user_page:user-page', self.kwargs['username'])
        return super().dispatch(request, *args, **kwargs)


# список понравившихся записей пользователя
class UserLikeList(View):
    template_name = 'user_page/like_list.html'
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
            'id': item.id,
            'username': item.author.username,
            'text': item.text,
            'tags': [str(tag) for tag in item.tags.all()],
            'created_at': created_at_month(datetime.strftime(item.updated_at, "%-d %B %Y г. %-H:%M")),
        }, 'profile': str(Profile.objects.get(user_id=item.author.id).photo.url) if Profile.objects.get(
            user_id=item.author.id).photo else None,
            'addition': self.__get_addition(item),}
            for item in items[page * self.__num_of_items:(page + 1) * self.__num_of_items]]

    def get(self, request, *args, **kwargs):
        page = int(request.GET.get('page', 1))
        likes = [record.item.id for record in
                   MarkedRecords.objects.filter(user=Profile.objects.get(user_id=User.objects.get(username=self.kwargs['username']).id),
                                                mark='Like').distinct()]
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            action = request.GET.get('action')
            items = Item.objects.filter(id__in=likes).order_by('-created_at').distinct()
            if action == 'feed':
                items_for_answer = self.__get_items(items, page)
                return JsonResponse({'all_data': items_for_answer, 'page': page})

        record = Profile.objects.get(user_id=User.objects.get(username=self.kwargs['username']).id)
        items = Item.objects.filter(id__in=likes).order_by('-created_at').distinct()
        user_items = [[item, Profile.objects.get(user_id=item.author.id), self.__get_addition(item)] for
                            item in items[:self.__num_of_items]]
        return render(request, self.template_name, {'user_items': user_items,'record': record, 'username': self.kwargs['username']})

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('registration:auth')
        return super().dispatch(request, *args, **kwargs)


# список подписок пользователя
def follows_list(request, username):
    if not request.user.is_authenticated:
        return redirect('registration:auth')
    record_subscription = Subscriptions.objects.get(subscriber_id=User.objects.get(username=username).id)
    all_records = list(record_subscription.subscription_profiles.all())
    if len(all_records) > 0:
        return render(request, 'user_page/follow_list.html', {'follows': all_records, 'username': username})
    return render(request, 'user_page/follow_list.html', {'follows': [], 'username': username})
