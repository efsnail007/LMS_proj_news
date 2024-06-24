from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView
from .models import Profile, Subscriptions
from .forms import UserPageEditForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.

class UserPageView(View):
    template_name = 'user_page/user_page.html'

    def __get_is_subscribed(self, request):
        record_subscription = Subscriptions.objects.get(subscriber_id=request.user.id)
        all_records = list(record_subscription.subscription_profiles.all())
        if len(all_records) > 0:
            for item in all_records:
                if str(item) == self.kwargs['username']:
                    return True
            return False
        return False

    def get(self, request, *args, **kwargs):
        record = Profile.objects.get(user_id=User.objects.get(username=self.kwargs['username']).id)
        return render(request, self.template_name, {'record': record, 'is_subscribed': self.__get_is_subscribed(request)})

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

