from enum import StrEnum
from typing import Any, Callable

from django.db.models import Q, QuerySet
from django.http import HttpRequest
from pydantic import BaseModel, ConfigDict

from .....utils.format import format_date, format_datetime, format_number, format_text, format_badge

class SortDirection(StrEnum):
    ASC = "asc"
    DESC = "desc"

class PaginationParam(BaseModel):
    page_index: int
    page_size: int
    sort: str
    sort_direction: SortDirection
    filters: list[Any]

    @classmethod
    def from_table_context(cls, ctx: 'TableContext'):
        params = {
            'page_index': int(ctx.request.GET.get('page_index', '0') or 0),
            'page_size': int(ctx.request.GET.get('page_size', '10') or 10),
        }
        params['filters'] = []
        for filter in ctx.filters:
            value = None
            if filter.type == FilterParam.Type.MULTISELECT:
                value = ctx.request.GET.getlist(filter.name, [])
            else:
                value = ctx.request.GET.get(filter.name, '')
            if value != '':
                params['filters'].append(filter.query(value))
        params['sort'] = ''
        params['sort_direction'] = 'asc'
        sort = ctx.request.GET.get('sort', '')
        if sort and any(column.sortable for column in ctx.columns if column.name == sort):
            params['sort'] = sort
            params['sort_direction'] = ctx.request.GET.get('sort_direction', 'asc')   
        return PaginationParam(**params)

class FilterParam(BaseModel):
    class Type(StrEnum):
        SELECT = "select"
        MULTISELECT = "multiselect"
        TEXT = "text"
        NUMBER = "number"
        BOOLEAN = "boolean"
        DATE = "date"
        DATETIME = "datetime"
        HIDDEN = "hidden"
    class Option(BaseModel):
        value: Any
        label: str
    name: str
    query: Callable[[Any], Any]
    label: str
    type: Type = Type.TEXT
    value: Any | None = None
    clearable: bool = True
    fetch_url: str | None = None

class TableColumn(BaseModel):
    class Type(StrEnum):
        TEXT = "text"
        BADGE = "badge"
        DATE = "date"
        DATETIME = "datetime"
        NUMBER = "number"
        BOOLEAN = "boolean"
        IMAGE = "image"

        @property
        def default_formatter(self):
            return {
                TableColumn.Type.DATE: lambda value: format_date(value),
                TableColumn.Type.DATETIME: lambda value: format_datetime(value),
                TableColumn.Type.NUMBER: lambda value: format_number(value),
                TableColumn.Type.TEXT: lambda value: format_text(value),
                TableColumn.Type.BOOLEAN: lambda value: format_badge(value),
                TableColumn.Type.BADGE: lambda value: format_badge(value),
            }.get(self, lambda value: value or '-')

    name: str
    label: str
    sortable: bool = False
    type: Type = Type.TEXT
    formatter: Callable[[Any], Any] | None = None
    need_tooltip: bool = False

    
    def format(self, value: Any):
        formatter = self.formatter or self.type.default_formatter
        return formatter(value) if formatter else value

# Not implemented yet
class TableAction(BaseModel):
    button: str
    

class TableContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    request: HttpRequest
    title: str | None = None
    partial_url: str
    columns: list[TableColumn]
    filters: list[FilterParam] = []
    actions: list[TableAction] = []
    row_actions: list[TableAction] = []
    bulk_actions: list = []

    def __create_data_context(self, data_set: QuerySet | list[Any], params: PaginationParam, transformer = None):
        if isinstance(data_set, QuerySet):
            and_filter = Q()
            for filter in params.filters:
                and_filter &= filter
            
            # Lấy ordering hiện tại TRƯỚC KHI filter (nếu có)
            # Đây là ordering mặc định từ query_set ban đầu (ví dụ: từ Meta.ordering hoặc order_by trong query)
            default_sort = []
            # Kiểm tra xem query_set có ordering không
            if hasattr(data_set.query, 'order_by') and data_set.query.order_by:
                default_sort = list(data_set.query.order_by)

            data_set = data_set.filter(and_filter)
            
            if params.sort:
                user_sort = ("-" if params.sort_direction == SortDirection.DESC else "") + params.sort
                # Tránh duplicate: chỉ thêm nếu chưa có trong default_order
                user_sort_normalized = user_sort.lstrip("-")
                duplicate_sort = next((
                    sort.lstrip("-") == user_sort_normalized 
                    for sort in default_sort
                ), None)
                if duplicate_sort:
                    # Thêm sort của user ra trước ordering mặc định
                    default_sort.remove(duplicate_sort)
                final_sort = [user_sort] + default_sort if default_sort else [user_sort]
                data_set = data_set.order_by(*final_sort) if final_sort else data_set
            else:
                # Nếu không có sort từ user, giữ nguyên ordering mặc định
                if default_sort:
                    data_set = data_set.order_by(*default_sort)
            
            total_count = data_set.count()
            page_rows = data_set.all()[params.page_index* params.page_size : (params.page_index + 1) * params.page_size]
            if transformer:
                page_rows = [transformer(row) for row in page_rows]
        else:
            # Filter not supported yet for list[Any]
            full_data = sorted(data_set, key=lambda x: x[params.sort], reverse=params.sort_direction == SortDirection.DESC) if params.sort else data_set
            total_count = len(full_data)
            page_rows = full_data[params.page_index* params.page_size : (params.page_index + 1) * params.page_size]
            if transformer:
                page_rows = [transformer(row) for row in page_rows]
        return {
            'total_count': total_count,
            'rows': page_rows,
            'page_index': params.page_index,
            'page_size': params.page_size,
            'sort': params.sort,
            'sort_direction': params.sort_direction,
        }

    def to_response_context(
        self,
        data_set: QuerySet | list[Any],
        transformer: Callable[[Any], Any] | None = None,
    ):
        params = PaginationParam.from_table_context(self)
        data_context = self.__create_data_context(data_set, params, transformer)
        return {
            **data_context,
            'request': self.request,
            'title': self.title,
            'partial_url': self.partial_url,
            'columns': self.columns,
            'filters': self.filters,
            'actions': self.actions,
            'bulk_actions': self.bulk_actions,
            'row_actions': self.row_actions,
            **data_context,
        }
