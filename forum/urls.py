
from django.conf.urls import patterns, url

from mezzanine.conf import settings


# Leading and trailing slahes for urlpatterns based on setup.
# _slashes = (
#     "/" if settings.FORUM_SLUG else "",
#     "/" if settings.APPEND_SLASH else "",
# )

# Forum patterns.
urlpatterns = patterns("forum.views",
    url(r"^feeds/(?P<format>.*)/$",
        "forum_post_feed", name="forum_post_feed"),
    url(r"^tag/(?P<tag>.*)/feeds/(?P<format>.*)/$",
        "forum_post_feed", name="forum_post_feed_tag"),
    url(r"^tag/(?P<tag>.*)/$", "forum_post_list",
        name="forum_post_list_tag"),
    url(r"^category/(?P<category>.*)/feeds/(?P<format>.*)/$",
        "forum_post_feed", name="forum_post_feed_category"),
    url(r"^category/(?P<category>.*)/$",
        "forum_post_list", name="forum_post_list_category"),
    url(r"^author/(?P<username>.*)/feeds/(?P<format>.*)/$",
        "forum_post_feed", name="forum_post_feed_author"),
    url(r"^author/(?P<username>.*)/$",
        "forum_post_list", name="forum_post_list_author"),
    url(r"^archive/(?P<year>\d{4})/(?P<month>\d{1,2})/$",
        "forum_post_list", name="forum_post_list_month"),
    url(r"^archive/(?P<year>\d{4})/$",
        "forum_post_list", name="forum_post_list_year"),
    url(r"^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/"
        "(?P<slug>.*)/$",
        "forum_post_detail", name="forum_post_detail_day"),
    url(r"^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>.*)/$",
        "forum_post_detail", name="forum_post_detail_month"),
    url(r"^(?P<year>\d{4})/(?P<slug>.*)/$",
        "forum_post_detail", name="forum_post_detail_year"),
    url(r"^(?P<slug>.*)/$", "forum_post_detail",
        name="forum_post_detail"),
    url(r"^$", "forum_post_list", name="forum_post_list"),
)
