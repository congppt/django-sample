from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import ListView


class UserListView(ListView):
    model = User
    template_name = "user/list.html"

    def get_context_data(self, **kwargs):
        request = self.request
        page = int(request.GET.get('page', '1') or 1)
        page_size = int(request.GET.get('page_size', '25') or 25)
        search = request.GET.get('search', '')
        is_active = request.GET.get('is_active', '')
        sort = request.GET.get('sort') or ''
        sort_direction = request.GET.get('sort_direction', 'asc')
        table_columns = [
            {"name": "name", "label": "Name", "sortable": True},
            {"name": "username", "label": "Username", "sortable": True},
            {
                "name": "date_joined",
                "label": "Registered",
                "type": "date",
                "sortable": True,
            },
            {
                "name": "is_active",
                "label": "Active",
                "type": "boolean",
                "sortable": True,
            },
        ]
        query_set = User.objects
        if is_active != '':
            query_set = query_set.filter(is_active=bool(is_active))
        if search:
            query_set = query_set.filter(username__icontains=search)
        if sort:
            query_set = query_set.order_by(("" if sort_direction == "asc" else "-") + sort)
        total_items = query_set.count()
        page_rows = query_set.all()[(page - 1) * page_size : page * page_size]
        total_pages = max((total_items + page_size - 1) // page_size, 1)
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "table_title": "Users",
                "data_url": reverse("user_list_partial"),
                # "export_url": reverse("user_list_export"),
                "table_columns": table_columns,
                "table_row_actions": [
                    {
                        "label": "View",
                        "url": "",
                        "icon": "eye",
                        "color": "blue",
                        "hx": True,
                    },
                    {"label": "Edit", "url": "", "icon": "edit", "color": "green"},
                    {"label": "Delete", "url": "", "icon": "close", "color": "red"},
                ],
                "bulk_actions": False,
                "table_filters": [
                    {
                        "name": "is_active",
                        "type": "select",
                        "options": [
                            {"value": "", "label": "All statuses"},
                            {"value": "true", "label": "Active"},
                            {"value": "false", "label": "Inactive"},
                        ],
                    },
                ],
                "search": search,
                "is_active": is_active,
                "table_data": page_rows,
                "total_items": total_items,
                "current_page": page,
                "page_size": page_size,
                "total_pages": (total_items + page_size - 1) // page_size,
                "start_item": (page - 1) * page_size + 1,
                "end_item": min(page * page_size, total_items),
                "visible_pages": list(range(max(1, page - 2), min(total_pages, page + 2) + 1)),
                "sort": sort,
                "sort_direction": sort_direction,
            }
        )
        return context

class UserListPartialView(ListView):
    model = User
    template_name = "templates/components/table.html"

    def get_context_data(self, **kwargs):
        request = self.request
        page = int(request.GET.get('page', '1') or 1)
        page_size = int(request.GET.get('page_size', '25') or 25)
        search = request.GET.get('search', '')
        is_active = request.GET.get('is_active', '')
        sort = request.GET.get('sort') or ''
        sort_direction = request.GET.get('sort_direction', 'asc')
        table_columns = [
            {"name": "name", "label": "Name", "sortable": True},
            {"name": "username", "label": "Username", "sortable": True},
            {
                "name": "date_joined",
                "label": "Registered",
                "type": "date",
                "sortable": True,
            },
            {
                "name": "is_active",
                "label": "Active",
                "type": "boolean",
                "sortable": True,
            },
        ]
        query_set = User.objects
        if is_active != '':
            query_set = query_set.filter(is_active=bool(is_active))
        if search:
            query_set = query_set.filter(username__icontains=search)
        if sort:
            query_set = query_set.order_by(("" if sort_direction == "asc" else "-") + sort)
        total_items = query_set.count()
        page_rows = query_set.all()[(page - 1) * page_size : page * page_size]
        total_pages = max((total_items + page_size - 1) // page_size, 1)
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "table_title": "Users",
                "data_url": reverse("user_list_partial"),
                # "export_url": reverse("user_list_export"),
                "table_columns": table_columns,
                "table_row_actions": [
                    {
                        "label": "View",
                        "url": "",
                        "icon": "eye",
                        "color": "blue",
                        "hx": True,
                    },
                    {"label": "Edit", "url": "", "icon": "edit", "color": "green"},
                    {"label": "Delete", "url": "", "icon": "close", "color": "red"},
                ],
                "bulk_actions": False,
                "table_filters": [
                    {
                        "name": "is_active",
                        "type": "select",
                        "options": [
                            {"value": "", "label": "All statuses"},
                            {"value": "true", "label": "Active"},
                            {"value": "false", "label": "Inactive"},
                        ],
                    },
                ],
                "search": search,
                "is_active": is_active,
                "table_data": page_rows,
                "total_items": total_items,
                "current_page": page,
                "page_size": page_size,
                "total_pages": (total_items + page_size - 1) // page_size,
                "start_item": (page - 1) * page_size + 1,
                "end_item": min(page * page_size, total_items),
                "visible_pages": list(range(max(1, page - 2), min(total_pages, page + 2) + 1)),
                "sort": sort,
                "sort_direction": sort_direction,
            }
        )
        return context