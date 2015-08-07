from datetime import datetime

from django.db.models import Count, Q

from calls.forms import CallsPostForm
from calls.models import CallsPost, CallsCategory
from mezzanine.generic.models import Keyword
from mezzanine import template
from mezzanine.utils.models import get_user_model

User = get_user_model()

register = template.Library()


@register.as_tag
def calls_months(*args):
    """
    Put a list of dates for calls posts into the template context.
    """
    dates = CallsPost.objects.published().values_list("publish_date", flat=True)
    date_dicts = [{"date": datetime(d.year, d.month, 1)} for d in dates]
    month_dicts = []
    for date_dict in date_dicts:
        if date_dict not in month_dicts:
            month_dicts.append(date_dict)
    for i, date_dict in enumerate(month_dicts):
        month_dicts[i]["post_count"] = date_dicts.count(date_dict)
    return month_dicts


@register.as_tag
def calls_categories(*args):
    """
    Put a list of categories for calls posts into the template context.
    """
    posts = CallsPost.objects.published()
    categories = CallsCategory.objects.filter(callsposts__in=posts)
    return list(categories.annotate(post_count=Count("callsposts")))


@register.as_tag
def calls_authors(*args):
    """
    Put a list of authors (users) for calls posts into the template context.
    """
    calls_posts = CallsPost.objects.published()
    authors = User.objects.filter(callsposts__in=calls_posts)
    return list(authors.annotate(post_count=Count("callsposts")))


@register.as_tag
def calls_recent_posts(limit=5, tag=None, username=None, category=None):
    """
    Put a list of recently published calls posts into the template
    context. A tag title or slug, category title or slug or author's
    username can also be specified to filter the recent posts returned.

    Usage::

        {% calls_recent_posts 5 as recent_posts %}
        {% calls_recent_posts limit=5 tag="django" as recent_posts %}
        {% calls_recent_posts limit=5 category="python" as recent_posts %}
        {% calls_recent_posts 5 username=admin as recent_posts %}

    """
    calls_posts = CallsPost.objects.published().select_related("user")
    title_or_slug = lambda s: Q(title=s) | Q(slug=s)
    if tag is not None:
        try:
            tag = Keyword.objects.get(title_or_slug(tag))
            calls_posts = calls_posts.filter(keywords__in=tag.assignments.all())
        except Keyword.DoesNotExist:
            return []
    if category is not None:
        try:
            category = CallsCategory.objects.get(title_or_slug(category))
            calls_posts = calls_posts.filter(categories=category)
        except CallsCategory.DoesNotExist:
            return []
    if username is not None:
        try:
            author = User.objects.get(username=username)
            calls_posts = calls_posts.filter(user=author)
        except User.DoesNotExist:
            return []
    return list(calls_posts[:limit])


@register.inclusion_tag("admin/includes/quick_calls.html", takes_context=True)
def quick_calls(context):
    """
    Admin dashboard tag for the quick calls form.
    """
    context["form"] = CallsPostForm()
    return context

# https://gist.github.com/renyi/3596248
from django import template
from django.utils import translation

from mezzanine.conf import settings


@register.filter
def get_object_translation(obj):
    # get current language
    lang = translation.get_language()

    try:
        # returns object with current translation
        for i in obj.translation.all():
            if i.lang == lang:
                return i
    except:
        pass

    # returns object without translation
    return obj