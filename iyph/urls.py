
from django.conf.urls import patterns, url

from mezzanine.conf import settings

from .views import ChronologyListView,ChronologyDetailView

# Leading and trailing slahes for urlpatterns based on setup.
# _slashes = (
#     "/" if settings.IYPH_SLUG else "",
#     "/" if settings.APPEND_SLASH else "",
# )

# iyph patterns.
urlpatterns = patterns("iyph.views",
    url(r"^feeds/(?P<format>.*)/$",    "iyph_post_feed", name="iyph_post_feed"),   
    url(r"^tag/(?P<tag>.*)/feeds/(?P<format>.*)/$","iyph_post_feed", name="iyph_post_feed_tag"),    
    url(r"^tag/(?P<tag>.*)/$", "iyph_post_list",name="iyph_post_list_tag"),
    url(r"^category/(?P<category>.*)/feeds/(?P<format>.*)/$",        "iyph_post_feed", name="iyph_post_feed_category"),
    url(r"^category/(?P<category>.*)/$",        "iyph_post_list", name="iyph_post_list_category"),
    url(r"^author/(?P<username>.*)/feeds/(?P<format>.*)/$",        "iyph_post_feed", name="iyph_post_feed_author"),
    url(r"^author/(?P<username>.*)/$",        "iyph_post_list", name="iyph_post_list_author"),
    url(r"^archive/(?P<year>\d{4})/(?P<month>\d{1,2})/$",        "iyph_post_list", name="iyph_post_list_month"),
    url(r"^archive/(?P<year>\d{4})/$",        "iyph_post_list", name="iyph_post_list_year"),
    url(r"^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>.*)/$",        "iyph_post_detail", name="iyph_post_detail_day"),
    url(r"^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>.*)/$",    "iyph_post_detail", name="iyph_post_detail_month"),
    url(r"^(?P<year>\d{4})/(?P<slug>.*)/$", "iyph_post_detail", name="iyph_post_detail_year"),
    url(r"^chronology/list/$", view=ChronologyListView.as_view(), name='chronology-list'),
    url(r"^chronology/list/(?P<slug>.*)/$", view=ChronologyDetailView.as_view(), name='chronology-detail'),
    url(r"^(?P<slug>.*)/$", "iyph_post_detail", name="iyph_post_detail"),
    url(r"^$", "iyph_post_list", name="iyph_post_list"),
  
    
)
