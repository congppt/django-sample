from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'home/home.html')

