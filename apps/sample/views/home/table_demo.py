from django.shortcuts import render
from django.urls import reverse


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
    for i in range(1, 123):
        rows.append({
            'id': i,
            'name': f'User {i}',
            'email': f'user{i}@example.com',
            'status': statuses[i % len(statuses)],
            'age': 20 + (i % 30),
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
        {'name': 'email', 'label': 'Email', 'sortable': True},
        {'name': 'status', 'label': 'Status', 'type': 'badge', 'sortable': True},
        {'name': 'age', 'label': 'Age', 'type': 'number', 'sortable': True},
    ]

    context = {
        'request': request,  # allow request.GET in template
        'table_title': 'HTMX Table Demo',
        'data_url': reverse('table_demo_partial'),
        'table_columns': table_columns,
        'table_row_actions': [],
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


