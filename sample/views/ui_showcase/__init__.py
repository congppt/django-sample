from django.urls import path
from .ui_showcase import UIShowcasePageView, ui_component_partial

urlpatterns = [
    path('', UIShowcasePageView.as_view(), name='ui_showcase'),
    path('components/<slug:component>/', ui_component_partial, name='ui_showcase_component'),
]