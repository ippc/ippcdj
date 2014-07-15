from datetime import datetime

from django.db.models import Count, Q

from forum.forms import ForumPostForm
from forum.models import ForumPost, ForumCategory
from mezzanine.generic.models import Keyword
from mezzanine import template
from mezzanine.utils.models import get_user_model

User = get_user_model()

register = template.Library()


@register.as_tag
def forum_months(*args):
    """
    Put a list of dates for forum posts into the template context.
    """
    dates = ForumPost.objects.published().values_list("publish_date", flat=True)
    date_dicts = [{"date": datetime(d.year, d.month, 1)} for d in dates]
    month_dicts = []
    for date_dict in date_dicts:
        if date_dict not in month_dicts:
            month_dicts.append(date_dict)
    for i, date_dict in enumerate(month_dicts):
        month_dicts[i]["post_count"] = date_dicts.count(date_dict)
    return month_dicts


@register.as_tag
def forum_categories(*args):
    """
    Put a list of categories for forum posts into the template context.
    """
    posts = ForumPost.objects.published()
    categories = ForumCategory.objects.filter(forumposts__in=posts)
    return list(categories.annotate(post_count=Count("forumposts")))


@register.as_tag
def forum_authors(*args):
    """
    Put a list of authors (users) for forum posts into the template context.
    """
    forum_posts = ForumPost.objects.published()
    authors = User.objects.filter(forumposts__in=forum_posts)
    return list(authors.annotate(post_count=Count("forumposts")))


@register.as_tag
def forum_recent_posts(limit=5, tag=None, username=None, category=None):
    """
    Put a list of recently published forum posts into the template
    context. A tag title or slug, category title or slug or author's
    username can also be specified to filter the recent posts returned.

    Usage::

        {% forum_recent_posts 5 as recent_posts %}
        {% forum_recent_posts limit=5 tag="django" as recent_posts %}
        {% forum_recent_posts limit=5 category="python" as recent_posts %}
        {% forum_recent_posts 5 username=admin as recent_posts %}

    """
    forum_posts = ForumPost.objects.published().select_related("user")
    title_or_slug = lambda s: Q(title=s) | Q(slug=s)
    if tag is not None:
        try:
            tag = Keyword.objects.get(title_or_slug(tag))
            forum_posts = forum_posts.filter(keywords__in=tag.assignments.all())
        except Keyword.DoesNotExist:
            return []
    if category is not None:
        try:
            category = ForumCategory.objects.get(title_or_slug(category))
            forum_posts = forum_posts.filter(categories=category)
        except ForumCategory.DoesNotExist:
            return []
    if username is not None:
        try:
            author = User.objects.get(username=username)
            forum_posts = forum_posts.filter(user=author)
        except User.DoesNotExist:
            return []
    return list(forum_posts[:limit])


@register.inclusion_tag("admin/includes/quick_forum.html", takes_context=True)
def quick_forum(context):
    """
    Admin dashboard tag for the quick forum form.
    """
    context["form"] = ForumPostForm()
    return context
