from calendar import month_name

from django.http import Http404
from django.shortcuts import get_object_or_404

from news.models import NewsPost, NewsCategory
from news.feeds import PostsRSS, PostsAtom
from mezzanine.conf import settings
from mezzanine.generic.models import Keyword
from mezzanine.utils.views import render, paginate
from mezzanine.utils.models import get_user_model

User = get_user_model()


def news_post_list(request, tag=None, year=None, month=None, username=None,
                   category=None, template="news/news_post_list.html"):
    """
    Display a list of news posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``news/news_post_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """
    settings.use_editable()
    templates = []
    news_posts = NewsPost.objects.published(for_user=request.user)
    if tag is not None:
        tag = get_object_or_404(Keyword, slug=tag)
        news_posts = news_posts.filter(keywords__in=tag.assignments.all())
    if year is not None:
        news_posts = news_posts.filter(publish_date__year=year)
        if month is not None:
            news_posts = news_posts.filter(publish_date__month=month)
            month = month_name[int(month)]
    if category is not None:
        category = get_object_or_404(NewsCategory, slug=category)
        news_posts = news_posts.filter(categories=category)
        templates.append(u"news/news_post_list_%s.html" %
                          unicode(category.slug))
    author = None
    if username is not None:
        author = get_object_or_404(User, username=username)
        news_posts = news_posts.filter(user=author)
        templates.append(u"news/news_post_list_%s.html" % username)

    prefetch = ("categories", "keywords__keyword")
    news_posts = news_posts.select_related("user").prefetch_related(*prefetch)
    news_posts = paginate(news_posts, request.GET.get("page", 1),
                          settings.NEWS_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    subscribed=0
 
    if category.id == 1:
        subscribed=request.user.groups.filter(name='News Notification group').exists()
    elif category.id == 3:
        subscribed=request.user.groups.filter(name='Announcement Notification group').exists()
    context = {"news_posts": news_posts, "year": year, "month": month,
               "tag": tag, "category": category, "author": author, "subscribed":subscribed, }
    
    templates.append(template)
  
    return render(request, templates, context)


def news_post_detail(request, slug, year=None, month=None, day=None,
                     template="news/news_post_detail.html"):
    """. Custom templates are checked for using the name
    ``news/news_post_detail_XXX.html`` where ``XXX`` is the news
    posts's slug.
    """
    news_posts = NewsPost.objects.published(
                                     for_user=request.user).select_related()
    news_post = get_object_or_404(news_posts, slug=slug)
    
    category_id=0 
    
    for c in news_post.categories.all():
       category_id=c.id
    
    subscribed=0
 
    if category_id == 1:
        subscribed=request.user.groups.filter(name='News Notification group').exists()
    elif category_id == 3:
        subscribed=request.user.groups.filter(name='Announcement Notification group').exists()
    context = {"news_post": news_post, "editable_obj": news_post,"subscribed":subscribed,"category":category_id}
    templates = [u"news/news_post_detail_%s.html" % unicode(slug), template]
    return render(request, templates, context)


def news_post_feed(request, format, **kwargs):
    """
    news posts feeds - maps format to the correct feed view.
    """
    try:
        return {"rss": PostsRSS, "atom": PostsAtom}[format](**kwargs)(request)
    except KeyError:
        raise Http404()
