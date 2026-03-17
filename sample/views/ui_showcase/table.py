from django.shortcuts import render

COLUMNS = [
    {'name': 'id', 'label': 'ID', 'sortable': True, 'formatter': lambda x: x},
    {'name': 'name', 'label': 'Name', 'sortable': True, 'formatter': lambda x: x},
    {'name': 'email', 'label': 'Email', 'sortable': True, 'formatter': lambda x: x},
    {'name': 'phone', 'label': 'Phone', 'sortable': True, 'formatter': lambda x: x},
    {'name': 'address', 'label': 'Address', 'sortable': True, 'formatter': lambda x: x},
    {'name': 'city', 'label': 'City', 'sortable': True, 'formatter': lambda x: x},
    {'name': 'state', 'label': 'State', 'sortable': True, 'formatter': lambda x: x.upper()},
]
DATA = [
    {
        'id': 1,
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'phone': '1234567890',
        'address': '123 Main St, Anytown, USA',
        'city': 'Anytown',
        'state': 'CA',
        'zip': '12345',
        'country': 'USA',
    },
    {
        'id': 2,
        'name': 'Jane Doe',
        'email': 'jane.doe@example.com',
        'phone': '0987654321',
        'address': '456 Main St, Anytown, USA',
        'city': 'Anytown',
        'state': 'CA',
    },
    {
        'id': 3,
        'name': 'Jim Beam',
        'email': 'jim.beam@example.com',
        'phone': '1234567890',
        'address': '123 Main St, Anytown, USA',
        'city': 'Anytown',
        'state': 'CA',
        'zip': '12345',
        'country': 'USA',
    },
    {
        'id': 4,
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'phone': '1234567890',
        'address': '123 Main St, Anytown, USA',
        'city': 'Anytown',
        'state': 'CA',
    },
    {
        'id': 5,
        'name': 'Jane Doe',
        'email': 'jane.doe@example.com',
        'phone': '0987654321',
        'address': '456 Main St, Anytown, USA',
        'city': 'Anytown',
        'state': 'CA',
    },
    {
        'id': 6,
        'name': 'Jim Beam',
        'email': 'jim.beam@example.com',
        'phone': '1234567890',
        'address': '123 Main St, Anytown, USA',
        'city': 'Anytown',
        'state': 'CA',
    },
]
def get_table_context(request):
    return render(request, 'ui_showcase/table.html', {'rows': DATA[:5], 'total_count': len(DATA), 'columns': COLUMNS})