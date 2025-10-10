import json
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment
from sample.templatetags.table_filters import get_badge_color
from datetime import date
from pydantic_core import to_jsonable_python

def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "static": staticfiles_storage.url,
            "url": reverse,
        }
    )

    def get_attribute(object, key):
        """Get item from dictionary by key"""
        if isinstance(object, dict):
            return object.get(key, "-")
        return getattr(object, key, "-")

    # Add custom filters
    env.filters["get_attribute"] = get_attribute
    env.filters["get_badge_color"] = get_badge_color

    # Add date formatting filter
    def strftime(value, format_string):
        if isinstance(value, date):
            return value.strftime(format_string)
        return value or "-"

    env.filters["strftime"] = strftime

    # Override tojson filter
    def tojson(value):
        return json.dumps(to_jsonable_python(value))

    env.filters["tojson"] = tojson

    return env
