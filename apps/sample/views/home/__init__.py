from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'home/home.html')

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    return render(request, 'home/login.html')