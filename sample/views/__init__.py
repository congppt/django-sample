from django.urls import include, path
from django.views.generic import RedirectView

from . import home

urlpatterns = [
    path('', RedirectView.as_view(url='home/'), name='root'),
    path('home/', include(home)),
]