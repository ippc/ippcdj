from calendar import month_name

from django.http import Http404
from django.shortcuts import get_object_or_404

from calls.models import CallsPost, CallsCategory
from calls.feeds import PostsRSS, PostsAtom
from mezzanine.conf import settings
from mezzanine.generic.models import Keyword
from mezzanine.utils.views import render, paginate
from mezzanine.utils.models import get_user_model

User = get_user_model()


def calls_post_list(request, tag=None, year=None, month=None, username=None,
                   category=None, template="calls/calls_post_list.html"):
    """
    Display a list of calls posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``calls/calls_post_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """
    settings.use_editable()
    templates = []
    calls_posts = CallsPost.objects.published(for_user=request.user)
    if tag is not None:
        tag = get_object_or_404(Keyword, slug=tag)
        calls_posts = calls_posts.filter(keywords__in=tag.assignments.all())
    if year is not None:
        calls_posts = calls_posts.filter(publish_date__year=year)
        if month is not None:
            calls_posts = calls_posts.filter(publish_date__month=month)
            month = month_name[int(month)]
    if category is not None:
        category = get_object_or_404(CallsCategory, slug=category)
        calls_posts = calls_posts.filter(categories=category)
        templates.append(u"calls/calls_post_list_%s.html" %
                          unicode(category.slug))
    author = None
    if username is not None:
        author = get_object_or_404(User, username=username)
        calls_posts = calls_posts.filter(user=author)
        templates.append(u"calls/calls_post_list_%s.html" % username)

    prefetch = ("categories", "keywords__keyword")
    calls_posts = calls_posts.select_related("user").prefetch_related(*prefetch)
    calls_posts = paginate(calls_posts, request.GET.get("page", 1),
                          settings.CALLS_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    subscribed=0
    subscribed=request.user.groups.filter(name='Calls Notification group').exists()
    context = {"calls_posts": calls_posts, "year": year, "month": month,
               "tag": tag, "category": category, "author": author, "subscribed":subscribed}
    templates.append(template)
    return render(request, templates, context)


def calls_post_detail(request, slug, year=None, month=None, day=None,
                     template="calls/calls_post_detail.html"):
    """. Custom templates are checked for using the name
    ``calls/calls_post_detail_XXX.html`` where ``XXX`` is the calls
    posts's slug.
    """
    calls_posts = CallsPost.objects.published(
                                     for_user=request.user).select_related()
    calls_post = get_object_or_404(calls_posts, slug=slug)
    subscribed=0
    subscribed=request.user.groups.filter(name='Calls Notification group').exists()

    context = {"calls_post": calls_post, "editable_obj": calls_post,"subscribed":subscribed}
    templates = [u"calls/calls_post_detail_%s.html" % unicode(slug), template]
    return render(request, templates, context)


def calls_post_feed(request, format, **kwargs):
    """
    calls posts feeds - maps format to the correct feed view.
    """
    try:
        return {"rss": PostsRSS, "atom": PostsAtom}[format](**kwargs)(request)
    except KeyError:
        raise Http404()
