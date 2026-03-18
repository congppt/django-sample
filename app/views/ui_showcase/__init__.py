from django.urls import path
from .ui_showcase import (
    UIShowcasePageView,
    ui_component_partial,
    ui_showcase_delay_demo,
    select_options_json,
)
from .table import TableListView, TableListPartialView, table_id_options_json

urlpatterns = [
    path('', UIShowcasePageView.as_view(), name='ui_showcase'),
    path('components/<slug:component>/', ui_component_partial, name='ui_showcase_component'),
    path('delay-demo/', ui_showcase_delay_demo, name='ui_showcase_delay_demo'),
    path('select-options', select_options_json, name='ui_showcase_select_options'),
    path('table-id-options', table_id_options_json, name='ui_showcase_table_id_options'),
    path('table/', TableListView.as_view(), name='ui_showcase_table'),
    path('table/partial/', TableListPartialView.as_view(), name='ui_showcase_table_partial'),
]