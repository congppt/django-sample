from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment
from sample.templatetags.table_filters import get_attribute, get_badge_color
from datetime import datetime


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    
    # Add custom filters
    env.filters['get_attribute'] = get_attribute
    env.filters['get_badge_color'] = get_badge_color
    
    # Add date formatting filter
    def strftime(value, format_string):
        if value and hasattr(value, 'strftime'):
            return value.strftime(format_string)
        return value
    
    env.filters['strftime'] = strftime
    
    return env
