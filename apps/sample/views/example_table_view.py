from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
import json

def example_table_view(request):
    """
    Example view showing how to use the advanced table component
    """
    
    # Sample data - replace with your actual model data
    sample_data = [
        {
            'id': 1,
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'role': 'Admin',
            'status': 'Active',
            'last_login': '2024-01-15 10:30:00',
            'created_at': '2024-01-01 09:00:00',
            'salary': 75000,
            'department': 'Engineering',
            'is_verified': True
        },
        {
            'id': 2,
            'name': 'Jane Smith',
            'email': 'jane.smith@example.com',
            'role': 'User',
            'status': 'Active',
            'last_login': '2024-01-14 15:45:00',
            'created_at': '2024-01-02 11:30:00',
            'salary': 65000,
            'department': 'Marketing',
            'is_verified': True
        },
        {
            'id': 3,
            'name': 'Bob Johnson',
            'email': 'bob.johnson@example.com',
            'role': 'Manager',
            'status': 'Inactive',
            'last_login': '2024-01-10 08:20:00',
            'created_at': '2024-01-03 14:15:00',
            'salary': 85000,
            'department': 'Sales',
            'is_verified': False
        },
        {
            'id': 4,
            'name': 'Alice Brown',
            'email': 'alice.brown@example.com',
            'role': 'User',
            'status': 'Active',
            'last_login': '2024-01-15 16:10:00',
            'created_at': '2024-01-04 10:45:00',
            'salary': 60000,
            'department': 'HR',
            'is_verified': True
        },
        {
            'id': 5,
            'name': 'Charlie Wilson',
            'email': 'charlie.wilson@example.com',
            'role': 'Admin',
            'status': 'Active',
            'last_login': '2024-01-15 12:30:00',
            'created_at': '2024-01-05 13:20:00',
            'salary': 90000,
            'department': 'Engineering',
            'is_verified': True
        },
        {
            'id': 6,
            'name': 'Diana Davis',
            'email': 'diana.davis@example.com',
            'role': 'User',
            'status': 'Pending',
            'last_login': None,
            'created_at': '2024-01-06 09:30:00',
            'salary': 55000,
            'department': 'Marketing',
            'is_verified': False
        },
        {
            'id': 7,
            'name': 'Eve Miller',
            'email': 'eve.miller@example.com',
            'role': 'Manager',
            'status': 'Active',
            'last_login': '2024-01-14 11:15:00',
            'created_at': '2024-01-07 15:45:00',
            'salary': 80000,
            'department': 'Finance',
            'is_verified': True
        },
        {
            'id': 8,
            'name': 'Frank Garcia',
            'email': 'frank.garcia@example.com',
            'role': 'User',
            'status': 'Active',
            'last_login': '2024-01-15 14:20:00',
            'created_at': '2024-01-08 12:10:00',
            'salary': 62000,
            'department': 'Engineering',
            'is_verified': True
        },
        {
            'id': 9,
            'name': 'Grace Lee',
            'email': 'grace.lee@example.com',
            'role': 'User',
            'status': 'Inactive',
            'last_login': '2024-01-12 09:45:00',
            'created_at': '2024-01-09 16:30:00',
            'salary': 58000,
            'department': 'HR',
            'is_verified': False
        },
        {
            'id': 10,
            'name': 'Henry Taylor',
            'email': 'henry.taylor@example.com',
            'role': 'Admin',
            'status': 'Active',
            'last_login': '2024-01-15 17:00:00',
            'created_at': '2024-01-10 08:15:00',
            'salary': 95000,
            'department': 'Engineering',
            'is_verified': True
        }
    ]
    
    # Table configuration
    table_columns = [
        {
            'name': 'name',
            'label': 'Full Name',
            'type': 'text',
            'sortable': True
        },
        {
            'name': 'email',
            'label': 'Email Address',
            'type': 'text',
            'sortable': True
        },
        {
            'name': 'role',
            'label': 'Role',
            'type': 'badge',
            'sortable': True
        },
        {
            'name': 'status',
            'label': 'Status',
            'type': 'badge',
            'sortable': True
        },
        {
            'name': 'department',
            'label': 'Department',
            'type': 'text',
            'sortable': True
        },
        {
            'name': 'salary',
            'label': 'Salary',
            'type': 'currency',
            'sortable': True
        },
        {
            'name': 'last_login',
            'label': 'Last Login',
            'type': 'datetime',
            'sortable': True
        },
        {
            'name': 'is_verified',
            'label': 'Verified',
            'type': 'boolean',
            'sortable': True
        }
    ]
    
    # Table actions (buttons in the header)
    table_actions = [
        {
            'label': 'Add User',
            'icon': 'plus.svg',
            'color': 'blue',
            'onclick': 'addUser()'
        },
        {
            'label': 'Export Data',
            'icon': 'export.svg',
            'color': 'green',
            'onclick': 'exportData()'
        },
        {
            'label': 'Bulk Actions',
            'icon': 'user-group.svg',
            'color': 'gray',
            'onclick': 'bulkActions()'
        }
    ]
    
    # Row actions (buttons for each row)
    table_row_actions = [
        {
            'label': 'View',
            'icon': 'eye.svg',
            'color': 'blue',
            'onclick': 'viewUser(this)'
        },
        {
            'label': 'Edit',
            'icon': 'edit.svg',
            'color': 'yellow',
            'onclick': 'editUser(this)'
        },
        {
            'label': 'Delete',
            'icon': 'close.svg',
            'color': 'red',
            'onclick': 'deleteUser(this)'
        }
    ]
    
    # Custom filters
    table_filters = [
        {
            'name': 'role',
            'label': 'Role',
            'options': [
                {'value': 'Admin', 'label': 'Admin'},
                {'value': 'Manager', 'label': 'Manager'},
                {'value': 'User', 'label': 'User'}
            ]
        },
        {
            'name': 'status',
            'label': 'Status',
            'options': [
                {'value': 'Active', 'label': 'Active'},
                {'value': 'Inactive', 'label': 'Inactive'},
                {'value': 'Pending', 'label': 'Pending'}
            ]
        },
        {
            'name': 'department',
            'label': 'Department',
            'options': [
                {'value': 'Engineering', 'label': 'Engineering'},
                {'value': 'Marketing', 'label': 'Marketing'},
                {'value': 'Sales', 'label': 'Sales'},
                {'value': 'HR', 'label': 'HR'},
                {'value': 'Finance', 'label': 'Finance'}
            ]
        }
    ]
    
    context = {
        'table_columns': table_columns,
        'table_data': sample_data,
        'table_actions': table_actions,
        'table_row_actions': table_row_actions,
        'table_filters': table_filters,
    }
    
    return render(request, 'templates/example_table.html', context)


def table_ajax_view(request):
    """
    AJAX endpoint for dynamic table data loading
    This can be used for server-side pagination, filtering, and sorting
    """
    if request.method == 'GET':
        # Get parameters from request
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 25))
        search = request.GET.get('search', '')
        sort_column = request.GET.get('sort_column', '')
        sort_direction = request.GET.get('sort_direction', 'asc')
        
        # Get filter parameters
        filters = {}
        for key, value in request.GET.items():
            if key.startswith('filter_') and value:
                filter_name = key.replace('filter_', '')
                filters[filter_name] = value
        
        # Here you would typically query your database
        # For this example, we'll use the same sample data
        sample_data = [
            # ... your data here (same as above)
        ]
        
        # Apply search filter
        if search:
            sample_data = [
                item for item in sample_data 
                if search.lower() in item['name'].lower() or 
                   search.lower() in item['email'].lower()
            ]
        
        # Apply custom filters
        for filter_name, filter_value in filters.items():
            sample_data = [
                item for item in sample_data 
                if item.get(filter_name) == filter_value
            ]
        
        # Apply sorting
        if sort_column and sort_column in sample_data[0] if sample_data else False:
            reverse = sort_direction == 'desc'
            sample_data.sort(key=lambda x: x[sort_column], reverse=reverse)
        
        # Apply pagination
        paginator = Paginator(sample_data, page_size)
        page_obj = paginator.get_page(page)
        
        # Prepare response data
        response_data = {
            'data': list(page_obj),
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'page_size': page_size,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            }
        }
        
        return JsonResponse(response_data)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
