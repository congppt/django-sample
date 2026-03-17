from django.contrib.auth.models import User
from django.shortcuts import  reverse
from django.views.generic import ListView

from utils.mock import name, email, phone, address

COLUMNS = [
    {'name': 'id', 'label': 'ID', 'sortable': True, 'formatter': lambda x: x},
    {'name': 'name', 'label': 'Name', 'sortable': True, 'formatter': lambda x: x.upper()},
    {'name': 'email', 'label': 'Email', 'sortable': True, 'formatter': lambda x: x},
    {'name': 'phone', 'label': 'Phone', 'sortable': False, 'formatter': lambda x: x},
    {'name': 'address', 'label': 'Addresssssss sssssssssssssssss ssssssssssssss sssssssssssssssss', 'sortable': True, 'formatter': lambda x: x},
]
DATA = []
if not DATA:
    for i in range(99):
        data = {
            'id': i,
            'phone': phone(),
            'address': address(),
        }
        data['name'] = name()
        data['email'] = email(data['name'])
        DATA.append(data)

def get_common_context(request):
    id = request.GET.get('id')
    filter_id = request.GET.get('filter_id')
    sort = request.GET.get('sort', '')
    sort_direction = request.GET.get('sort_direction', '')
    page_index = int(request.GET.get('page_index', 0))
    page_size = int(request.GET.get('page_size', 10))
    data = sorted(DATA, key=lambda x: x[sort], reverse=sort_direction == 'desc') if sort else DATA
    total_count = len(data)
    return {
        'id': id,
        'filter_id': filter_id,
        'columns': COLUMNS,
        'rows': data[page_index * page_size:min((page_index + 1) * page_size, total_count)],
        'sort': sort,
        'sort_direction': sort_direction,
        'partial_url': reverse('ui_showcase_table_partial'),
        'page_index': page_index,
        'page_size': page_size,
        'total_count': total_count,
    }

class TableListView(ListView):
    model = User
    template_name = "ui_showcase/table.html"

    def get_context_data(self, **kwargs):
        return get_common_context(self.request)

class TableListPartialView(ListView):
    model = User
    template_name = "ui_showcase/table_partial.html"

    def get_context_data(self, **kwargs):
        return get_common_context(self.request)