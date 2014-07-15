
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import Atom1Feed
from django.utils.html import strip_tags

from forum.models import ForumPost, ForumCategory
from mezzanine.generic.models import Keyword
from mezzanine.pages.models import Page
from mezzanine.conf import settings
from mezzanine.utils.models import get_user_model

User = get_user_model()


class PostsRSS(Feed):
    """
    RSS feed for all forum posts.
    """

    def __init__(self, *args, **kwargs):
        """
        Use the title and description of the Forum page for the feed's
        title and description. If the forum page has somehow been
        removed, fall back to the ``SITE_TITLE`` and ``SITE_TAGLINE``
        settings.
        """
        self.tag = kwargs.pop("tag", None)
        self.category = kwargs.pop("category", None)
        self.username = kwargs.pop("username", None)
        super(PostsRSS, self).__init__(*args, **kwargs)
        self._public = True
        try:
            page = Page.objects.published().get(slug=settings.FORUM_SLUG)
        except Page.DoesNotExist:
            page = None
        else:
            self._public = not page.login_required
        if self._public:
            settings.use_editable()
            if page is not None:
                self._title = "%s | %s" % (page.title, settings.SITE_TITLE)
                self._description = strip_tags(page.description)
            else:
                self._title = settings.SITE_TITLE
                self._description = settings.SITE_TAGLINE

    def title(self):
        return self._title

    def description(self):
        return self._description

    def link(self):
        return reverse("forum_post_feed", kwargs={"format": "rss"})

    def items(self):
        if not self._public:
            return []
        forum_posts = ForumPost.objects.published().select_related("user")
        if self.tag:
            tag = get_object_or_404(Keyword, slug=self.tag)
            forum_posts = forum_posts.filter(keywords__in=tag.assignments.all())
        if self.category:
            category = get_object_or_404(ForumCategory, slug=self.category)
            forum_posts = forum_posts.filter(categories=category)
        if self.username:
            author = get_object_or_404(User, username=self.username)
            forum_posts = forum_posts.filter(user=author)
        limit = settings.FORUM_RSS_LIMIT
        if limit is not None:
            forum_posts = forum_posts[:settings.FORUM_RSS_LIMIT]
        return forum_posts

    def item_description(self, item):
        return item.content

    def categories(self):
        if not self._public:
            return []
        return ForumCategory.objects.all()

    def item_author_name(self, item):
        return item.user.get_full_name() or item.user.username

    def item_author_link(self, item):
        username = item.user.username
        return reverse("forum_post_list_author", kwargs={"username": username})

    def item_pubdate(self, item):
        return item.publish_date

    def item_categories(self, item):
        return item.categories.all()


class PostsAtom(PostsRSS):
    """
    Atom feed for all forum posts.
    """

    feed_type = Atom1Feed

    def subtitle(self):
        return self.description()

    def link(self):
        return reverse("forum_post_feed", kwargs={"format": "atom"})
