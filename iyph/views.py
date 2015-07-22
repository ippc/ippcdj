from calendar import month_name

from django.http import Http404
from django.shortcuts import get_object_or_404

from iyph.models import IyphPost, IyphCategory
from iyph.feeds import PostsRSS, PostsAtom
from mezzanine.conf import settings
from mezzanine.generic.models import Keyword
from mezzanine.utils.views import render, paginate
from mezzanine.utils.models import get_user_model

User = get_user_model()


def iyph_post_list(request, tag=None, year=None, month=None, username=None,
                   category=None, template="iyph/iyph_post_list.html"):
    """
    Display a list of iyph posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``iyph/iyph_post_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """
    settings.use_editable()
    templates = []
    iyph_posts = IyphPost.objects.published(for_user=request.user)
    if tag is not None:
        tag = get_object_or_404(Keyword, slug=tag)
        iyph_posts = iyph_posts.filter(keywords__in=tag.assignments.all())
    if year is not None:
        iyph_posts = iyph_posts.filter(publish_date__year=year)
        if month is not None:
            iyph_posts = iyph_posts.filter(publish_date__month=month)
            month = month_name[int(month)]
    if category is not None:
        category = get_object_or_404(IyphCategory, slug=category)
        iyph_posts = iyph_posts.filter(categories=category)
        templates.append(u"iyph/iyph_post_list_%s.html" %
                          unicode(category.slug))
    author = None
    if username is not None:
        author = get_object_or_404(User, username=username)
        iyph_posts = iyph_posts.filter(user=author)
        templates.append(u"iyph/iyph_post_list_%s.html" % username)

    prefetch = ("categories", "keywords__keyword")
    iyph_posts = iyph_posts.select_related("user").prefetch_related(*prefetch)
    iyph_posts = paginate(iyph_posts, request.GET.get("page", 1),
                          settings.IYPH_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    context = {"iyph_posts": iyph_posts, "year": year, "month": month,
               "tag": tag, "category": category, "author": author}
    templates.append(template)
    return render(request, templates, context)


def iyph_post_detail(request, slug, year=None, month=None, day=None,
                     template="iyph/iyph_post_detail.html"):
    """. Custom templates are checked for using the name
    ``iyph/iyph_post_detail_XXX.html`` where ``XXX`` is the iyph
    posts's slug.
    """
    iyph_posts = IyphPost.objects.published(
                                     for_user=request.user).select_related()
    iyph_post = get_object_or_404(iyph_posts, slug=slug)
    context = {"iyph_post": iyph_post, "editable_obj": iyph_post}
    templates = [u"iyph/iyph_post_detail_%s.html" % unicode(slug), template]
    return render(request, templates, context)


def iyph_post_feed(request, format, **kwargs):
    """
    iyph posts feeds - maps format to the correct feed view.
    """
    try:
        return {"rss": PostsRSS, "atom": PostsAtom}[format](**kwargs)(request)
    except KeyError:
        raise Http404()
