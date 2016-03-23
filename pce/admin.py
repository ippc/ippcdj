# https://gist.github.com/renyi/3596248
from copy import deepcopy
from django.contrib import admin
from mezzanine.pages.models import Page, RichTextPage, Link
from mezzanine.pages.admin import PageAdmin, LinkAdmin
from mezzanine.conf import settings
from mezzanine.core.admin import TabularDynamicInlineAdmin, StackedDynamicInlineAdmin,DisplayableAdmin, OwnableAdmin



from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory
from django.contrib.auth.models import User
from django import forms


from django_markdown.admin import MarkdownModelAdmin


import autocomplete_light
#import autocomplete_light_registry

#from django_markdown.widgets  import MarkdownWidget


#from django.contrib.auth.admin import UserAdmin

