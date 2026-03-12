from django.urls import path
from .ui_showcase import UIShowcasePageView

urlpatterns = [
    path('', UIShowcasePageView.as_view(), name='ui_showcase')
]