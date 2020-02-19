
from django.conf.urls import patterns, url

from mezzanine.conf import settings
from mezzanine.pages.models import RichTextPage

from .views import ChronologyListView,ChronologyDetailView,Page1View,Page2View,chronology_create,chronology_edit,PhotoLibraryView,PhotoListView,PhotoHiddenDetailView,\
PhotoDetailView,photo_create,IYPHPageView
from mezzanine.core.views import direct_to_template
# Leading and trailing slahes for urlpatterns based on setup.
# _slashes = (
#     "/" if settings.IYPH_SLUG else "",
#     "/" if settings.APPEND_SLASH else "",
# )

# iyph patterns.
urlpatterns = patterns("iyph.views",
    #---------POST ------------------------------#    
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
    #---------EVENTS ------------------------------# 
   # url(r'^chronologies/(?P<type>\d+)/create/$', view=chronology_create, name='chronology-create'),
   # url(r'^chronologies/(?P<id>\d+)/edit/$',        view=chronology_edit,        name='chronology-edit'),
   # url(r'^chronology/list/$',view=ChronologyListView.as_view(),  name='chronology-list'),
   # url(r"^chronology/(?P<slug>.*)/$", view=ChronologyDetailView.as_view(), name='chronology-detail'),
    #---------committee ------------------------------# 
    url(r"^iyphisc/$", view=Page2View.as_view(), name='page-2-detail'),
    url(r"^iyphtab/$", view=Page1View.as_view(), name='page-1-detail'),
   
    
   #---------PHOTO ------------------------------# 
   
    url(r"^photo/(?P<pk>.*)/$", view=PhotoDetailView.as_view(), name="photo-detail"),
    url(r"^photolibrary/(?P<slug>[\w-]+)/$", view=PhotoLibraryView.as_view(), name="photo-library-detail"),
    url(r"^photo-pending/$", view=PhotoListView.as_view(), name="photo-pending"),
    url(r"^photo-hidden/(?P<pk>.*)/$", view=PhotoHiddenDetailView.as_view(), name="photo-detail-non-approved"),
    url(r'^photo-submit/$', view=photo_create, name='photo-create'),
    #---------PAGE ------------------------------#    
    url(r"^(?P<slug>[\w-]+)/$", view=IYPHPageView.as_view(), name="iyphpage-detail"),
   
   
    #---------AUTO-REGISTER-USER ------------------------------#    
    #url(r'^accounts/pendingapproval/$',PhotoAutoRegistrationListView.as_view(), name='index'),
    #url(r'^accounts/autoregister/$',view=auto_register_photo,name='auto-register'),
    #url(r'^accounts/autoregister/approve/(?P<id>\d+)/$',view=auto_register_photo_approve,name='auto-register-photo-approve'),
    #url(r'^accounts/autoregister/delete/(?P<id>\d+)/$',view=auto_register_photo_delete,name='auto-register-photo-delete'),
    #url(r'^accounts/requestaccess/$',view=requestaccess,name='request-acccess'),
 
    url(r"^(?P<slug>.*)/$", "iyph_post_detail", name="iyph_post_detail"),
    url(r"^$", "homeview", name="homeview"),
    url(r"^postlist$", "iyph_post_list", name="iyph_post_list_l"),
   
    
    #url("^$", direct_to_template, {"template": "index1.html"}, name="hoame"),
  




    
)
