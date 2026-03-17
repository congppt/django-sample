from django.shortcuts import render

from utils.mock import name, email, phone, address

COLUMNS = [
    {'name': 'id', 'label': 'ID', 'sortable': True, 'formatter': lambda x: x},
    {'name': 'name', 'label': 'Name', 'sortable': True, 'formatter': lambda x: x.upper()},
    {'name': 'email', 'label': 'Email', 'sortable': True, 'formatter': lambda x: x},
    {'name': 'phone', 'label': 'Phone', 'sortable': True, 'formatter': lambda x: x},
    {'name': 'address', 'label': 'Address', 'sortable': True, 'formatter': lambda x: x},
]
DATA = []
if not DATA:
    for i in range(100):
        data = {
            'id': i,
            'phone': phone(),
            'address': address(),
        }
        data['name'] = name()
        data['email'] = email(data['name'])
        DATA.append(data)
def get_table_context(request):
    return render(request, 'ui_showcase/table.html', {'rows': DATA[:5], 'total_count': len(DATA), 'columns': COLUMNS})