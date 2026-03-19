from django.contrib.messages import get_messages
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment

from utils.json import jsonify


def environment(**options):
    env = Environment(**options)
    def get_attribute(object, key, default=None):
        """Get item from dictionary by key"""
        if isinstance(object, dict):
            return object.get(key, default)
        return getattr(object, key, default)

    env.globals.update(
        {
            "static": staticfiles_storage.url,
            "url": reverse,
            "jsonify": jsonify,
            "get_attribute": get_attribute,
            "get_messages": get_messages,
        }
    )

    return env
