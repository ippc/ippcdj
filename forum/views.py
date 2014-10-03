from calendar import month_name

from django.http import Http404
from django.shortcuts import get_object_or_404

from forum.models import ForumPost, ForumCategory,ForumPost_Files
from ippc.models import IppcUserProfile
from forum.feeds import PostsRSS, PostsAtom
from mezzanine.conf import settings
from mezzanine.generic.models import Keyword
from mezzanine.utils.views import render, paginate
from mezzanine.utils.models import get_user_model

User = get_user_model()


def forum_post_list(request, tag=None, year=None, month=None, username=None,
                   category=None, template="forum/forum_post_list.html"):
    """
    Display a list of forum posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``forum/forum_post_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """
    settings.use_editable()
    templates = []
    forum_posts = ForumPost.objects.published(for_user=request.user)
    if tag is not None:
        tag = get_object_or_404(Keyword, slug=tag)
        forum_posts = forum_posts.filter(keywords__in=tag.assignments.all())
    if year is not None:
        forum_posts = forum_posts.filter(publish_date__year=year)
        if month is not None:
            forum_posts = forum_posts.filter(publish_date__month=month)
            month = month_name[int(month)]
    if category is not None:
        category = get_object_or_404(ForumCategory, slug=category)
        forum_posts = forum_posts.filter(categories=category)
        templates.append(u"forum/forum_post_list_%s.html" %
                          unicode(category.slug))
    author = None
    if username is not None:
        author = get_object_or_404(User, username=username)
        forum_posts = forum_posts.filter(user=author)
        templates.append(u"forum/forum_post_list_%s.html" % username)

    prefetch = ("categories", "keywords__keyword")
    forum_posts = forum_posts.select_related("user").prefetch_related(*prefetch)
    forum_posts = paginate(forum_posts, request.GET.get("page", 1),
                          settings.FORUM_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    context = {"forum_posts": forum_posts, "year": year, "month": month,
               "tag": tag, "category": category, "author": author}
    templates.append(template)
    return render(request, templates, context)

from collections import defaultdict

def forum_post_detail(request, slug, year=None, month=None, day=None,
                     template="forum/forum_post_detail.html"):
    """. Custom templates are checked for using the name
    ``forum/forum_post_detail_XXX.html`` where ``XXX`` is the forum
    posts's slug.
    """
    forum_posts = ForumPost.objects.published(
                                     for_user=request.user).select_related()
    forum_post = get_object_or_404(forum_posts, slug=slug)
    
    #forum_post_files = get_object_or_404(forum_posts, slug=slug)
    f = get_object_or_404(ForumPost, slug=slug)
    files = ForumPost_Files.objects.filter( forum_post_id=f.id)
    
    context = {"forum_post": forum_post, "editable_obj": forum_post,"files":files}
    templates = [u"forum/forum_post_detail_%s.html" % unicode(slug), template]
    return render(request, templates, context)


def forum_post_feed(request, format, **kwargs):
    """
    Forum posts feeds - maps format to the correct feed view.
    """
    try:
        return {"rss": PostsRSS, "atom": PostsAtom}[format](**kwargs)(request)
    except KeyError:
        raise Http404()
