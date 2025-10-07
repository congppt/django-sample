from django.http import HttpResponseRedirect
from django.shortcuts import render


def home(request):
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect('login/')
    return render(request, 'home/home.html')

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('home/')
    else:
        return render(request, 'home/login.html')