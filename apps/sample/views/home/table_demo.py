from django.shortcuts import render
from django.urls import reverse
from django.http import FileResponse
from django.http import Http404
from datetime import date, datetime, timedelta
import csv
import io


def _paginate(total_items: int, page: int, page_size: int):
    total_pages = max((total_items + page_size - 1) // page_size, 1)
    page = max(1, min(page, total_pages))
    start_index = (page - 1) * page_size
    end_index = min(start_index + page_size, total_items)
    start_item = 0 if total_items == 0 else start_index + 1
    end_item = end_index

    # visible pages (max 5)
    max_visible = 5
    start = max(1, page - max_visible // 2)
    end = min(total_pages, start + max_visible - 1)
    if end - start + 1 < max_visible:
        start = max(1, end - max_visible + 1)
    visible_pages = list(range(start, end + 1))

    return {
        'current_page': page,
        'page_size': page_size,
        'total_pages': total_pages,
        'start_item': start_item,
        'end_item': end_item,
        'visible_pages': visible_pages,
    }


def _mock_rows():
    rows = []
    statuses = ['Active', 'Inactive', 'Pending']
    cities = ['New York', 'London', 'Tokyo', 'Berlin', 'Paris', 'Sydney']
    countries = ['USA', 'UK', 'Japan', 'Germany', 'France', 'Australia']
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Support']
    roles = ['Admin', 'Manager', 'User', 'Guest']
    for i in range(1, 123):
        rows.append({
            'id': i,
            'name': f'User {i}',
            'username': f'user{i:03d}',
            'email': f'user{i}@example.com',
            'phone': f"+1-555-{1000 + i}",
            'status': statuses[i % len(statuses)],
            'age': 20 + (i % 30),
            'city': cities[i % len(cities)],
            'country': countries[i % len(countries)],
            'department': departments[i % len(departments)],
            'role': roles[i % len(roles)],
            'company': f'ExampleCo {i % 7}',
            'address': f'{100 + i} Main St',
            'registered_on': date.today() - timedelta(days=i % 365),
            'last_login': datetime.now() - timedelta(days=i % 30, hours=i % 24),
            'balance': f"${(i * 13) % 10000}.{(i * 37) % 100:02d}",
            'active': (i % 2 == 0),
            'score': (i * 7) % 100,
        })
    return rows


def _filter_sort_rows(rows, search: str, sort: str, sort_direction: str, status: str, min_age: str, max_age: str):
    if search:
        s = search.lower()
        rows = [r for r in rows if s in r['name'].lower() or s in r['email'].lower()]
    if status:
        rows = [r for r in rows if r['status'] == status]
    if min_age:
        try:
            mn = int(min_age)
            rows = [r for r in rows if int(r['age']) >= mn]
        except ValueError:
            pass
    if max_age:
        try:
            mx = int(max_age)
            rows = [r for r in rows if int(r['age']) <= mx]
        except ValueError:
            pass
    if sort:
        reverse = (sort_direction or 'asc') == 'desc'
        rows = sorted(rows, key=lambda r: r.get(sort), reverse=reverse)
    return rows


def _common_context(request):
    page = int(request.GET.get('page', '1') or 1)
    page_size = int(request.GET.get('page_size', '25') or 25)
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    min_age = request.GET.get('min_age', '')
    max_age = request.GET.get('max_age', '')
    sort = request.GET.get('sort') or ''
    sort_direction = request.GET.get('sort_direction', 'asc')

    all_rows = _filter_sort_rows(_mock_rows(), search, sort, sort_direction, status, min_age, max_age)
    total_items = len(all_rows)

    pg = _paginate(total_items, page, page_size)
    page_rows = all_rows[(pg['current_page'] - 1) * page_size: (pg['current_page'] - 1) * page_size + page_size]

    table_columns = [
        {'name': 'name', 'label': 'Name', 'sortable': True},
        {'name': 'username', 'label': 'Username', 'sortable': True},
        {'name': 'email', 'label': 'Email', 'sortable': True},
        {'name': 'phone', 'label': 'Phone', 'sortable': False},
        {'name': 'status', 'label': 'Status', 'type': 'badge', 'sortable': True},
        {'name': 'age', 'label': 'Age', 'type': 'number', 'sortable': True},
        {'name': 'city', 'label': 'City', 'sortable': True},
        {'name': 'country', 'label': 'Country', 'sortable': True},
        {'name': 'department', 'label': 'Department', 'sortable': True},
        {'name': 'role', 'label': 'Role', 'sortable': True},
        {'name': 'company', 'label': 'Company', 'sortable': True},
        {'name': 'address', 'label': 'Address', 'sortable': False},
        {'name': 'registered_on', 'label': 'Registered', 'type': 'date', 'sortable': True},
        {'name': 'last_login', 'label': 'Last Login', 'type': 'datetime', 'sortable': True},
        {'name': 'balance', 'label': 'Balance', 'type': 'currency', 'sortable': False, 'align': 'end'},
        {'name': 'active', 'label': 'Active', 'type': 'boolean', 'sortable': True},
        {'name': 'score', 'label': 'Score', 'type': 'number', 'sortable': True},
    ]

    context = {
        'request': request,  # allow request.GET in template
        'table_title': 'HTMX Table Demo',
        'data_url': reverse('table_demo_partial'),
        'export_url': reverse('table_demo_export'),
        'table_columns': table_columns,
        'table_row_actions': [
            { 'label': 'View', 'url': 'table_demo_detail', 'icon': 'eye', 'color': 'blue', 'hx': True },
            { 'label': 'Edit', 'url': '', 'icon': 'edit', 'color': 'green' },
            { 'label': 'Delete', 'url': '', 'icon': 'close', 'color': 'red' },
        ],
        'bulk_actions': False,
        'table_filters': [
            {
                'name': 'status',
                'type': 'select',
                'options': [
                    {'value': '', 'label': 'All statuses'},
                    {'value': 'Active', 'label': 'Active'},
                    {'value': 'Inactive', 'label': 'Inactive'},
                    {'value': 'Pending', 'label': 'Pending'},
                ],
            },
            {'name': 'min_age', 'type': 'number'},
            {'name': 'max_age', 'type': 'number'},
        ],
        'search': search,
        'status': status,
        'min_age': min_age,
        'max_age': max_age,
        'table_data': page_rows,
        'total_items': total_items,
        'current_page': pg['current_page'],
        'page_size': pg['page_size'],
        'total_pages': pg['total_pages'],
        'start_item': pg['start_item'],
        'end_item': pg['end_item'],
        'visible_pages': pg['visible_pages'],
        'sort': sort,
        'sort_direction': sort_direction,
    }
    return context


def page(request):
    context = _common_context(request)
    return render(request, 'home/table_demo.html', context)


def partial(request):
    context = _common_context(request)
    return render(request, 'templates/components/table.html', context)


def export(request):
    """Export endpoint - handles both HTMX redirect and direct file download"""
    # Check if this is an HTMX request
    is_htmx = request.headers.get('HX-Request') == 'true'
    
    if is_htmx:
        # HTMX request - redirect to the same endpoint for file download
        from django.http import HttpResponse
        
        # Build the download URL with all current parameters
        params = request.GET.urlencode()
        download_url = request.build_absolute_uri() + '?' + params
        
        # Return empty response with HX-Redirect header
        response = HttpResponse()
        response['HX-Redirect'] = download_url
        return response
    
    # Direct file download request
    # Get filtered data (same logic as _common_context but without pagination)
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    min_age = request.GET.get('min_age', '')
    max_age = request.GET.get('max_age', '')
    sort = request.GET.get('sort') or ''
    sort_direction = request.GET.get('sort_direction', 'asc')
    
    all_rows = _filter_sort_rows(_mock_rows(), search, sort, sort_direction, status, min_age, max_age)
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    headers = ['ID', 'Name', 'Username', 'Email', 'Phone', 'Status', 'Age', 'City', 'Country', 
               'Department', 'Role', 'Company', 'Address', 'Registered On', 'Last Login', 
               'Balance', 'Active', 'Score']
    writer.writerow(headers)
    
    # Write data rows
    for row in all_rows:
        writer.writerow([
            row['id'],
            row['name'],
            row['username'],
            row['email'],
            row['phone'],
            row['status'],
            row['age'],
            row['city'],
            row['country'],
            row['department'],
            row['role'],
            row['company'],
            row['address'],
            row['registered_on'].strftime('%Y-%m-%d'),
            row['last_login'].strftime('%Y-%m-%d %H:%M'),
            row['balance'],
            'Yes' if row['active'] else 'No',
            row['score']
        ])
    
    # Create file-like object from CSV content
    csv_content = output.getvalue()
    output.close()
    
    # Create FileResponse
    file_obj = io.BytesIO(csv_content.encode('utf-8'))
    response = FileResponse(file_obj, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="table_export.csv"'
    
    return response

# new view: detail
def detail(request, id: int):
    rows = _mock_rows()
    row = next((r for r in rows if r['id'] == id), None)
    if not row:
        raise Http404('Record not found')
    ctx = {
        'title': f"User - {row['name']}",
        'user': {
            'name': row['name'],
            'email': row['email'],
            'phone': row['phone'],
            'status': row['status'],
        },
    }
    return render(request, 'home/detail_demo.html', ctx)
