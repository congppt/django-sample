from django.urls import include, path
from django.views.generic import RedirectView

from . import home, ui_showcase

urlpatterns = [
    path('', RedirectView.as_view(url='home/'), name='root'),
    path('home/', include(home)),
    path('ui-showcase/', include(ui_showcase)),
]