from django.urls import path

from . import home, login
from . import table_demo

urlpatterns = [
    path('', home, name='home'),
    path('login', login, name='login'),
    path('table-demo', table_demo.page, name='table_demo'),
    path('table-demo/partial', table_demo.partial, name='table_demo_partial'),
    path('table-demo/export', table_demo.export, name='table_demo_export'),
    path('table-demo/detail/<int:id>', table_demo.detail, name='table_demo_detail'),
    path('table-demo/modal-content', table_demo.modal_content, name='table_demo_modal_content'),
]