import json
from datetime import date, datetime

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.utils import translation
from django.middleware.csrf import get_token
from jinja2 import Environment
from pydantic_core import to_jsonable_python



def environment(**options):
    env = Environment(extensions=['jinja2.ext.i18n'], **options)
    env.install_gettext_translations(translation)
    
    env.globals.update(
        {
            "static": staticfiles_storage.url,
            "url": reverse,
        }
    )

    def get_attribute(object, key, default=None):
        """Get item from dictionary by key"""
        if isinstance(object, dict):
            return object.get(key, default)
        return getattr(object, key, default)

    # 
    env.filters["get_attribute"] = get_attribute

    def jsonify(value):
        return json.dumps(to_jsonable_python(value))

    env.filters["jsonify"] = jsonify

    return env
