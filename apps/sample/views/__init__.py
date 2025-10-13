from django.http import HttpResponseRedirect
from django.urls import reverse


def index(_):
    return HttpResponseRedirect(reverse('home'))