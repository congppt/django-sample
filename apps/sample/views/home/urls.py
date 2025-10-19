from django.urls import path

from . import home

urlpatterns = [
    path('', home, name='home'),

]