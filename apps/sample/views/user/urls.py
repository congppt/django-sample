from django.urls import path
from . import UserListPartialView, UserListView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('partial/', UserListPartialView.as_view(), name='user_list_partial'),
]