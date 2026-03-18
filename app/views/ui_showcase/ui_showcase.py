import time

from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render, reverse
from django.views.generic.base import TemplateView

ASSET_TYPE_OPTIONS = [
    {"value": "land", "label": "Đất"},
    {"value": "car", "label": "Ô tô"},
    {"value": "house", "label": "Nhà, vật kiến trúc"},
    {"value": "machinery", "label": "Thiết bị máy móc"},
    {"value": "other", "label": "Tài sản khác"},
    {"value": "perennial", "label": "Cây lâu năm, súc vật làm việc và cho sản phẩm"},
    {"value": "long1", "label": "Tài sản cố định hữu hình khác (máy móc, thiết bị, phương tiện vận tải, dụng cụ quản lý) và tài sản cố định vô hình"},
    {"value": "long2", "label": "Cây lâu năm, súc vật làm việc và cho sản phẩm, và các tài sản cố định khác có thời gian sử dụng trên 12 tháng"},
]

def select_options_json(request):
    return JsonResponse(ASSET_TYPE_OPTIONS, safe=False)


class UIShowcasePageView(TemplateView):
    template_name = "ui_showcase/ui_showcase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        component = self.request.GET.get('component', 'tooltip')
        context['template_name'] = COMPONENT_TEMPLATES.get(component)
        if not context['template_name']:
            raise Http404("Unknown UI component")
        return context


def ui_showcase_delay_demo(request):
    time.sleep(3.5)
    return HttpResponse("<p class=\"text-sm text-slate-600\">Request completed.</p>")


COMPONENT_TEMPLATES = {
    "tooltip": "ui_showcase/tooltip.html",
    "button": "ui_showcase/button.html",
    "select": "ui_showcase/select.html",
    "input": "ui_showcase/input.html",
    "table": "ui_showcase/table.html",
}


def ui_component_partial(request, component: str):
    template_name = COMPONENT_TEMPLATES.get(component)
    if not template_name:
        raise Http404("Unknown UI component")
    context = {}
    if component == "table":
        return redirect(reverse('ui_showcase_table'))
    return render(request, template_name, context)