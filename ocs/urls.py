from django.conf.urls import patterns, include, url
from mezzanine.core.views import direct_to_template

# from ocs import views

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {"template": "ocs/home.html"}, name="home"),
    url(r'^upload/$', direct_to_template, {"template": "upload.html"}, name="upload"),
    url(r'^detail/$', direct_to_template, {"template": "detail.html"}, name="detail"),
    # url(r'^$', views.IndexView.as_view(), name='index'),
    # url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    # url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    # url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)