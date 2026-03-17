from django.urls import path
from .ui_showcase import (
    UIShowcasePageView,
    ui_component_partial,
    ui_showcase_delay_demo,
    select_options_json,
)
from .table import get_table_context

urlpatterns = [
    path('', UIShowcasePageView.as_view(), name='ui_showcase'),
    path('components/<slug:component>/', ui_component_partial, name='ui_showcase_component'),
    path('delay-demo/', ui_showcase_delay_demo, name='ui_showcase_delay_demo'),
    path('select-options', select_options_json, name='ui_showcase_select_options'),
    path('table/', get_table_context, name='ui_showcase_table'),
]