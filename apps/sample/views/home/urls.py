from django.urls import path

from . import home, login
urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
]