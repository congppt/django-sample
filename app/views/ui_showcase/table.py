from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import reverse
from django.views.generic import ListView

from ..templates.components.button import Button
from ..templates.components.table import TableContext, TableAction, FilterParam, TableColumn
from utils.mock import name, email, phone, address

COLUMNS = [
    TableColumn(
        name='id',
        label='ID',
        sortable=True,
    ),
    TableColumn(
        name='name',
        label='Name',
        sortable=True,
    ),
    TableColumn(
        name='email',
        label='Email',
        sortable=True,
    ),
    TableColumn(
        name='phone',
        label='Phone',
        sortable=False,
    ),
    TableColumn(
        name='address',
        label='Address',
        sortable=True,
    ),
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
    # Prefill the select UI with the active `id` query param (if any).
    # This helps the dropdown show the currently selected label.
    raw_id = request.GET.get("id")
    try:
        id_value = int(raw_id) if raw_id not in (None, "") else None
    except (TypeError, ValueError):
        id_value = None

    table_context = TableContext(
        request=request,
        title='Table showcase',
        columns=COLUMNS,
        filters=[
            FilterParam(
                name='id',
                label='ID',
                placeholder='Select ID',
                type=FilterParam.Type.SELECT,
                value=id_value,
                query=lambda value: (lambda target: str(target.get('id')) == str(value)),
                extra_attributes={
                    "options_url": reverse('ui_showcase_table_id_options'),
                },
            ),
            FilterParam(
                name='name',
                label='Name',
                placeholder='Enter name',
                type=FilterParam.Type.TEXT,
                query=lambda value: (lambda target: target['name'].startswith(value)),
            ),
            FilterParam(
                name='email',
                label='Email', 
                placeholder='Enter email',
                type=FilterParam.Type.TEXT,
                query=lambda value: (lambda target: target['email'].startswith(value))
            ),
            FilterParam(
                name='phone',
                label='Phone',
                placeholder='Enter phone',
                type=FilterParam.Type.TEXT,
                query=lambda value: (lambda target: target['phone'].startswith(value))
            ),
            FilterParam(
                name='address',
                label='Address',
                placeholder='Enter address',
                type=FilterParam.Type.TEXT,
                query=lambda value: (lambda target: target['address'].startswith(value))
            ),
        ],
        partial_url=reverse('ui_showcase_table_partial'),
        actions=[
            TableAction(
                label='Add',
                icon='plus.svg',
                icon_position=Button.IconPosition.LEFT,
                variant=Button.Variant.FILLED,
                disabled=False,
                loading_text='Adding...',
                href="https://google.com",
            ),
            TableAction(
                label='Edit',
                icon='edit.svg',
                icon_position=Button.IconPosition.LEFT,
                variant=Button.Variant.OUTLINED,
                disabled=False,
                loading_text='Editing...',
                extra_attributes={
                    'hx-get': reverse('ui_showcase_component', kwargs={'component': 'select'}),
                    'hx-target': '#ui-showcase-content',
                    'hx-swap': 'innerHTML',
                },
            ),
            TableAction(
                label='Delete',
                icon='trash.svg',
                icon_position=Button.IconPosition.LEFT,
                variant=Button.Variant.OUTLINED,
                disabled=False,
                loading_text='Deleting...',
                extra_attributes={
                    '@click': f'''$dispatch("modal:open", 
                     {{ 
                        url: "{reverse("ui_showcase_component", kwargs={'component': 'table'})}", 
                        title: "Modal showcase",
                        ariaLabel: "Aria label" 
                    }} 
                    );'''
                }
            )
        ]
    )
    return {
        **table_context.to_response_context(DATA),
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


def table_id_options_json(request):
    """Return table ID options for the `id` filter select."""
    options = [{"value": i, "label": str(i)} for i in range(99)]
    return JsonResponse(options, safe=False)