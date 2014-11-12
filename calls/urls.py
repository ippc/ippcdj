
from django.conf.urls import patterns, url

from mezzanine.conf import settings


# Leading and trailing slahes for urlpatterns based on setup.
# _slashes = (
#     "/" if settings.calls_SLUG else "",
#     "/" if settings.APPEND_SLASH else "",
# )

# calls patterns.
urlpatterns = patterns("calls.views",
    url(r"^feeds/(?P<format>.*)/$",
        "calls_post_feed", name="calls_post_feed"),
    url(r"^tag/(?P<tag>.*)/feeds/(?P<format>.*)/$",
        "calls_post_feed", name="calls_post_feed_tag"),
    url(r"^tag/(?P<tag>.*)/$", "calls_post_list",
        name="calls_post_list_tag"),
    url(r"^category/(?P<category>.*)/feeds/(?P<format>.*)/$",
        "calls_post_feed", name="calls_post_feed_category"),
    url(r"^category/(?P<category>.*)/$",
        "calls_post_list", name="calls_post_list_category"),
    url(r"^author/(?P<username>.*)/feeds/(?P<format>.*)/$",
        "calls_post_feed", name="calls_post_feed_author"),
    url(r"^author/(?P<username>.*)/$",
        "calls_post_list", name="calls_post_list_author"),
    url(r"^archive/(?P<year>\d{4})/(?P<month>\d{1,2})/$",
        "calls_post_list", name="calls_post_list_month"),
    url(r"^archive/(?P<year>\d{4})/$",
        "calls_post_list", name="calls_post_list_year"),
    url(r"^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/"
        "(?P<slug>.*)/$",
        "calls_post_detail", name="calls_post_detail_day"),
    url(r"^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>.*)/$",
        "calls_post_detail", name="calls_post_detail_month"),
    url(r"^(?P<year>\d{4})/(?P<slug>.*)/$",
        "calls_post_detail", name="calls_post_detail_year"),
    url(r"^(?P<slug>.*)/$", "calls_post_detail",
        name="calls_post_detail"),
    url(r"^$", "calls_post_list", name="calls_post_list"),
)
