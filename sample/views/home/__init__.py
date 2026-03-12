from django.urls import path
from .home import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home')
]