from django.urls import path
from item import views

app_name = 'item'

urlpatterns = [
    path('add/', views.NewsCreationView.as_view(), name='item-add'),
    path('<int:item_id>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('<int:item_id>/update/', views.ItemUpdateView.as_view(), name='update_item'),
    path('<int:item_id>/delete/', views.ItemDeleteView.as_view(), name='delete_item'),
    path('<int:item_id>/feedback/', views.FeedbackView.as_view(), name='feedback'),
]
