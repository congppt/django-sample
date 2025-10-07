from django.http import HttpResponseRedirect


def index(_):
    return HttpResponseRedirect('home/')