import time

from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView


class UIShowcasePageView(TemplateView):
    template_name = "ui_showcase/ui_showcase.html"


def ui_showcase_delay_demo(request):
    time.sleep(3.5)
    return HttpResponse("<p class=\"text-sm text-slate-600\">Request completed.</p>")


COMPONENT_TEMPLATES = {
    "tooltip": "ui_showcase/tooltip.html",
    "button": "ui_showcase/button.html",
}


def ui_component_partial(request, component: str):
    template_name = COMPONENT_TEMPLATES.get(component)
    if not template_name:
        raise Http404("Unknown UI component")
    return render(request, template_name)

