from django.contrib.auth.models import User
from django.shortcuts import  reverse
from django.views.generic import ListView

from ..templates.components.button import Button
from ..templates.components.table import TableContext, TableAction
from utils.mock import name, email, phone, address

COLUMNS = [
    {'name': 'id', 'label': 'ID', 'sortable': True, 'formatter': lambda x: x},
    {'name': 'name', 'label': 'Name', 'sortable': True, 'formatter': lambda x: x.upper()},
    {'name': 'email', 'label': 'Email', 'sortable': True, 'formatter': lambda x: x},
    {'name': 'phone', 'label': 'Phone', 'sortable': False, 'formatter': lambda x: x},
    {'name': 'address', 'label': 'Address', 'sortable': True, 'formatter': lambda x: x},
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
    table_context = TableContext(
        request=request,
        title='Table showcase',
        columns=COLUMNS,
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
                    '@click': '$dispatch("modal:open", { "url": "https://google.com" });console.log("modal opened")'
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