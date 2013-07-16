# https://gist.github.com/renyi/3596248
from django import template
from django.utils import translation

from mezzanine.conf import settings

register = template.Library()

@register.filter
def get_object_translation(obj):
    # get current language
    lang = translation.get_language()
    # path = request.path
    # lang = translation.get_language_from_path('path')

    try:
        # returns object with current translation
        for i in obj.translation.all():
            if i.lang == lang:
                return i
    except:
        pass

    # returns object without translation
    return obj