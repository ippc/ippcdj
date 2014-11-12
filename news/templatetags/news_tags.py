from datetime import datetime

from django.db.models import Count, Q

from news.forms import NewsPostForm
from news.models import NewsPost, NewsCategory
from mezzanine.generic.models import Keyword
from mezzanine import template
from mezzanine.utils.models import get_user_model

User = get_user_model()

register = template.Library()


@register.as_tag
def news_months(*args):
    """
    Put a list of dates for news posts into the template context.
    """
    dates = NewsPost.objects.published().values_list("publish_date", flat=True)
    date_dicts = [{"date": datetime(d.year, d.month, 1)} for d in dates]
    month_dicts = []
    for date_dict in date_dicts:
        if date_dict not in month_dicts:
            month_dicts.append(date_dict)
    for i, date_dict in enumerate(month_dicts):
        month_dicts[i]["post_count"] = date_dicts.count(date_dict)
    return month_dicts


@register.as_tag
def news_categories(*args):
    """
    Put a list of categories for news posts into the template context.
    """
    posts = NewsPost.objects.published()
    categories = NewsCategory.objects.filter(newsposts__in=posts)
    return list(categories.annotate(post_count=Count("newsposts")))


@register.as_tag
def news_authors(*args):
    """
    Put a list of authors (users) for news posts into the template context.
    """
    news_posts = NewsPost.objects.published()
    authors = User.objects.filter(newsposts__in=news_posts)
    return list(authors.annotate(post_count=Count("newsposts")))


@register.as_tag
def news_recent_posts(limit=5, tag=None, username=None, category=None):
    """
    Put a list of recently published news posts into the template
    context. A tag title or slug, category title or slug or author's
    username can also be specified to filter the recent posts returned.

    Usage::

        {% news_recent_posts 5 as recent_posts %}
        {% news_recent_posts limit=5 tag="django" as recent_posts %}
        {% news_recent_posts limit=5 category="python" as recent_posts %}
        {% news_recent_posts 5 username=admin as recent_posts %}

    """
    news_posts = NewsPost.objects.published().select_related("user")
    title_or_slug = lambda s: Q(title=s) | Q(slug=s)
    if tag is not None:
        try:
            tag = Keyword.objects.get(title_or_slug(tag))
            news_posts = news_posts.filter(keywords__in=tag.assignments.all())
        except Keyword.DoesNotExist:
            return []
    if category is not None:
        try:
            category = NewsCategory.objects.get(title_or_slug(category))
            news_posts = news_posts.filter(categories=category)
        except NewsCategory.DoesNotExist:
            return []
    if username is not None:
        try:
            author = User.objects.get(username=username)
            news_posts = news_posts.filter(user=author)
        except User.DoesNotExist:
            return []
    return list(news_posts[:limit])


@register.inclusion_tag("admin/includes/quick_news.html", takes_context=True)
def quick_news(context):
    """
    Admin dashboard tag for the quick news form.
    """
    context["form"] = NewsPostForm()
    return context
