from django.urls import path
from user_page import views

app_name = 'user_page'

urlpatterns = [
    path('<slug:username>/', views.UserPageView.as_view(), name='user-page'),
    path('<slug:username>/edit/', views.UserPageViewEdit.as_view(), name='user-page-edit'),
    path('<slug:username>/follows/', views.follows_list, name='follows'),
]