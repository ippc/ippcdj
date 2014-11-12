
from django.conf.urls import patterns, url

from mezzanine.conf import settings


# Leading and trailing slahes for urlpatterns based on setup.
# _slashes = (
#     "/" if settings.news_SLUG else "",
#     "/" if settings.APPEND_SLASH else "",
# )

# news patterns.
urlpatterns = patterns("news.views",
    url(r"^feeds/(?P<format>.*)/$",
        "news_post_feed", name="news_post_feed"),
    url(r"^tag/(?P<tag>.*)/feeds/(?P<format>.*)/$",
        "news_post_feed", name="news_post_feed_tag"),
    url(r"^tag/(?P<tag>.*)/$", "news_post_list",
        name="news_post_list_tag"),
    url(r"^category/(?P<category>.*)/feeds/(?P<format>.*)/$",
        "news_post_feed", name="news_post_feed_category"),
    url(r"^category/(?P<category>.*)/$",
        "news_post_list", name="news_post_list_category"),
    url(r"^author/(?P<username>.*)/feeds/(?P<format>.*)/$",
        "news_post_feed", name="news_post_feed_author"),
    url(r"^author/(?P<username>.*)/$",
        "news_post_list", name="news_post_list_author"),
    url(r"^archive/(?P<year>\d{4})/(?P<month>\d{1,2})/$",
        "news_post_list", name="news_post_list_month"),
    url(r"^archive/(?P<year>\d{4})/$",
        "news_post_list", name="news_post_list_year"),
    url(r"^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/"
        "(?P<slug>.*)/$",
        "news_post_detail", name="news_post_detail_day"),
    url(r"^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>.*)/$",
        "news_post_detail", name="news_post_detail_month"),
    url(r"^(?P<year>\d{4})/(?P<slug>.*)/$",
        "news_post_detail", name="news_post_detail_year"),
    url(r"^(?P<slug>.*)/$", "news_post_detail",
        name="news_post_detail"),
    url(r"^$", "news_post_list", name="news_post_list"),
)
