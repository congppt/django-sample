import json

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.middleware.csrf import get_token
from jinja2 import Environment
from pydantic_core import to_jsonable_python

from utils.mock import number


def environment(**options):
    env = Environment(**options)
    def jsonify(value):
        return json.dumps(to_jsonable_python(value))
    def get_attribute(object, key, default=None):
        """Get item from dictionary by key"""
        if isinstance(object, dict):
            return object.get(key, default)
        return getattr(object, key, default)
    def random_id(prefix: str):
        return f"{prefix}-{number(1000, 9999)}"

    env.globals.update(
        {
            "static": staticfiles_storage.url,
            "url": reverse,
            "jsonify": jsonify,
            "get_attribute": get_attribute,
            "random_id": random_id,
        }
    )

    return env
