from django.conf.urls import patterns, include, url
from mezzanine.core.views import direct_to_template
from django.contrib.auth.decorators import login_required

# from ocs import views

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {"template": "ocs/home.html"}, name="home"),
    url(r'^upload/$', direct_to_template, {"template": "ocs/upload.html"}, name="upload"),
    url(r'^001-test-document-detail/$', login_required(direct_to_template), {"template": "ocs/detail.html"}, name="detail"),
    # url(r'^$', views.IndexView.as_view(), name='index'),
    # url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    # url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    # url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)