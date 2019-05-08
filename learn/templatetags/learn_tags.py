from django import template  
#from django.template import Library, Node

from django.db.models import get_model
from .translate_tags import get_object_translation
from django.shortcuts import get_object_or_404
from settings import MEDIA_URL
import os.path


import urllib, cStringIO, base64

register = template.Library()

@register.filter
def get64(url):
    """
    Method returning base64 image data instead of URL
    """
    if url.startswith("http"):
        image = cStringIO.StringIO(urllib.urlopen(url).read())
        return 'data:image/jpg;base64,' + base64.b64encode(image.read())

    return url



