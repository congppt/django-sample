from django.urls import path

from . import page, partial, export, detail

urlpatterns = [
    path('table-demo', page, name='table_demo'),
    path('table-demo/partial', partial, name='table_demo_partial'),
    path('table-demo/export', export, name='table_demo_export'),
    path('table-demo/detail/<int:id>', detail, name='table_demo_detail'),
]