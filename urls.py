
from django.conf.urls import patterns, include, url
from django.contrib import admin

from .ippc.views import PestReportListView, PestReportHiddenListView, \
PestReportDetailView, CountryView, pest_report_create, pest_report_edit, PublicationDetailView,\
PublicationListView,ReportingObligationListView, ReportingObligationDetailView,reporting_obligation_create, reporting_obligation_edit, \
EventReportingListView, EventReportingDetailView,event_reporting_create, event_reporting_edit, \
PestFreeAreaListView, PestFreeAreaDetailView,pfa_create, pfa_edit, WebsiteListView, WebsiteDetailView ,website_create, website_edit, \
ImplementationISPMListView, ImplementationISPMDetailView,implementationispm_create, implementationispm_edit,CountryListView,\
AdvancesSearchCNListView,CnPublicationListView,CnPublicationDetailView,country_publication_create,country_publication_edit
from schedule.periods import Year, Month, Week, Day
from mezzanine.core.views import direct_to_template
import mezzanine_pagedown.urls
import autocomplete_light
autocomplete_light.autodiscover()
admin.autodiscover()

# Add the urlpatterns for any custom Django applications here.
# You can also change the ``home`` view to add your own functionality
# to the project's homepage.

urlpatterns = patterns("",
    
    url(r'^ocs/', include('ocs.urls', namespace="ocs")),

    url(r'^forum/', include('forum.urls')),

    # forum detail
    # url(r'^forum/(?P<slug>[\w-]+)/$',
    #     view=ForumPostDetailView.as_view(),
    #     name="forum-post-detail"),
    
    url("^sitemap/$", direct_to_template, {"template": "sitemap.html"}, name="sitemap"),
    url("^contact/$", direct_to_template, {"template": "contact.html"}, name="contact"),
    # url("^feeds/$", direct_to_template, {"template": "feeds.html"}, name="feeds"),
    # url("^legal/$", direct_to_template, {"template": "legal.html"}, name="legal"),
    # url("^colophon/$", direct_to_template, {"template": "colophon.html"}, name="colophon"),
    # url("^faq/$", direct_to_template, {"template": "sitemap.html"}, name="sitemap"),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^events/', include('schedule.urls')),
    url(r'^month/(?P<calendar_slug>[-\w]+)/$',
        'schedule.views.calendar_by_periods',
        name="month_calendar",
        kwargs={'periods': [Month], 'template_name': 'schedule/calendar_month.html'}),
    url(r'^event/create/(?P<calendar_slug>[-\w]+)/$',
        'schedule.views.create_or_edit_event',
        name='calendar_create_event'),
    url(r'^year/(?P<calendar_slug>[-\w]+)/$',
        'schedule.views.calendar_by_year',
        name="year_calendar",
        kwargs={'year': [Year], 'template_name': 'schedule/calendar_year.html'}),

      
  # countries
    
    # individual country home
    url(r'^countries/(?P<country>[\w-]+)/$',
        view=CountryView.as_view(),
        # view=country_view(),
        name='country'),
    # countries list by region or all
    url(r'^countries/(?P<region>[\w-]+)/list-countries/$',
        view=CountryListView.as_view(),
        # view=country_view(),
        name='country-list'),
    # advanced results of reporting list
    url(r'^countries/(?P<type>[\w-]+)$',
        view=AdvancesSearchCNListView.as_view(),
        name='advsearch'),
    #-------------------------------------------#    
    # pest report list
    url(r'^countries/(?P<country>[\w-]+)/pestreports/$',
        view=PestReportListView.as_view(),
        name='pest-report-list'),

    # pest list showing hidden reports 
    url(r'^countries/(?P<country>[\w-]+)/pestreports/hidden/$',
        view=PestReportHiddenListView.as_view(),
        name='pest-report-hidden-list'),

    # pest report detail
    url(r'^countries/(?P<country>[\w-]+)/pestreports/(?P<year>\d+)/(?P<month>\d{2})/(?P<slug>[\w-]+)/$',
        view=PestReportDetailView.as_view(),
        name="pest-report-detail"),
        
    # pest report create
    url(r'^countries/(?P<country>[\w-]+)/pestreports/create/$',
        view=pest_report_create,
        name='pest-report-create'),
    
    # pest report edit
    # url(r'^countries/(?P<country>[\w-]+)/pestreports/(?P<year>\d+)/(?P<month>\d{2})/(?P<slug>[\w-]+)/edit/$',
    url(r'^countries/(?P<country>[\w-]+)/pestreports/edit/(?P<id>\d+)/$',
        view=pest_report_edit,
        name='pest-report-edit'),
#-------------------------------------------#
    # publication list
    url(r'^publications/$',
        view=PublicationListView.as_view(),
        name='publication-list'),

    # publication detail
    url(r'^publications/(?P<pk>\d+)/$',
        view=PublicationDetailView.as_view(),
        name='publication-detail'),
    #-------------------------------------------#
 
    #-------------------------------------------#
    
    # reporting obligation list
    url(r'^countries/(?P<country>[\w-]+)/reportingobligation/$',
        view=ReportingObligationListView.as_view(),
        name='reporting-obligation-list'),

    # reporting obligation list showing hidden reports 
    #url(r'^countries/(?P<country>[\w-]+)/reportingobligation/hidden/$',
    #    view=ReportingObligationHiddenListView.as_view(),
    #    name='reporting-obligation-hidden-list'),
     # testmodel create
     
    
    # reporting obligation detail
    url(r'^countries/(?P<country>[\w-]+)/reportingobligation/(?P<year>\d+)/(?P<month>\d{2})/(?P<slug>[\w-]+)/$',
        view=ReportingObligationDetailView.as_view(),
        name="reporting-obligation-detail"),
     # reporting obligation create
    url(r'^countries/(?P<country>[\w-]+)/reportingobligation/(?P<type>[\w-]+)/create/$',
        view=reporting_obligation_create,
        name='reporting-obligation-create'),
    # reporting obligation edit
    url(r'^countries/(?P<country>[\w-]+)/reportingobligation/edit/(?P<id>\d+)/$',
        view=reporting_obligation_edit,
        name='reporting-obligation-edit'),
    #-------------------------------------------#
    # event reporting list
    url(r'^countries/(?P<country>[\w-]+)/eventreporting/$',
        view=EventReportingListView.as_view(),
        name='event-reporting-list'),

    # event reporting list showing hidden reports 
    #url(r'^countries/(?P<country>[\w-]+)/eventreporting/hidden/$',
    #    view=EventReportingHiddenListView.as_view(),
    #    name='event-reporting-hidden-list'),

    # event reporting detail
    url(r'^countries/(?P<country>[\w-]+)/eventreporting/(?P<year>\d+)/(?P<month>\d{2})/(?P<slug>[\w-]+)/$',
        view=EventReportingDetailView.as_view(),
        name="event-reporting-detail"),
        
     # event reporting create
    url(r'^countries/(?P<country>[\w-]+)/eventreporting/(?P<type>[\w-]+)/create/$',
        view=event_reporting_create,
        name='event-reporting-create'),
        
    # event reporting edit
    url(r'^countries/(?P<country>[\w-]+)/eventreporting/edit/(?P<id>\d+)/$',
        view=event_reporting_edit,
        name='event-reporting-edit'),


    # event reporting list
    url(r'^countries/(?P<country>[\w-]+)/eventreporting/$',
        view=EventReportingListView.as_view(),
        name='event-reporting-list'),
 #-------------------------------------------#
    # website list
    url(r'^countries/(?P<country>[\w-]+)/websites/$',
        view=WebsiteListView.as_view(),
        name='website-list'),

    #website list showing hidden reports 
    #url(r'^countries/(?P<country>[\w-]+)/websites/hidden/$',
    #    view=WebsitesHiddenListView.as_view(),
    #    name='website-hidden-list'),

    # website detail
    url(r'^countries/(?P<country>[\w-]+)/websites/(?P<year>\d+)/(?P<month>\d{2})/(?P<slug>[\w-]+)/$',
        view=WebsiteDetailView.as_view(),
        name="website-detail"),
        
     # websitecreate
    url(r'^countries/(?P<country>[\w-]+)/websites/create/$',
        view=website_create,
        name='website-create'),
        
    # website edit
    url(r'^countries/(?P<country>[\w-]+)/websites/edit/(?P<id>\d+)/$',
        view=website_edit,
        name='website-edit'),


#-------------------------------------------#
    # CN publications list
    url(r'^countries/(?P<country>[\w-]+)/publications/$',
        view=CnPublicationListView.as_view(),
        name='country-publication-list'),

    #CN publications list showing hidden reports 
    #url(r'^countries/(?P<country>[\w-]+)/websites/hidden/$',
    #    view=WebsitesHiddenListView.as_view(),
    #    name='website-hidden-list'),

    # CN publications detail
    url(r'^countries/(?P<country>[\w-]+)/publications/(?P<year>\d+)/(?P<month>\d{2})/(?P<slug>[\w-]+)/$',
        view=CnPublicationDetailView.as_view(),
        name="country-publication-detail"),
        
     # CN publications create
    url(r'^countries/(?P<country>[\w-]+)/publications/create/$',
        view=country_publication_create,
        name='country-publication-create'),
        
    # CN publications edit
    url(r'^countries/(?P<country>[\w-]+)/publications/edit/(?P<id>\d+)/$',
        view=country_publication_edit,
        name='country-publication-edit'),
    # event reporting list showing hidden reports 
    #url(r'^countries/(?P<country>[\w-]+)/eventreporting/hidden/$',
    #    view=EventReportingHiddenListView.as_view(),
    #    name='event-reporting-hidden-list'),

#-------------------------------------------#
   # pfa list
    url(r'^countries/(?P<country>[\w-]+)/pestfreeareas/$',
        view=PestFreeAreaListView.as_view(),
        name='pfa-list'),

    # pfa list showing hidden reports 
    #url(r'^countries/(?P<country>[\w-]+)/eventreportings/hidden/$',
    #    view=EventReportingHiddenListView.as_view(),
    #    name='event-reporting-hidden-list'),

    # pfa reporting detail
    url(r'^countries/(?P<country>[\w-]+)/pestfreeareas/(?P<year>\d+)/(?P<month>\d{2})/(?P<slug>[\w-]+)/$',
        view=PestFreeAreaDetailView.as_view(),
        name="pfa-detail"),
        
     # pfa create
    url(r'^countries/(?P<country>[\w-]+)/pestfreeareas/create/$',
        view=pfa_create,
        name='pfa-create'),
        
    # pfa edit
    url(r'^countries/(?P<country>[\w-]+)/pestfreeareas/edit/(?P<id>\d+)/$',
        view=pfa_edit,
        name='pfa-edit'),

#-------------------------------------------#




# ImplementationISPM list
    url(r'^countries/(?P<country>[\w-]+)/implementationispm/$',
        view=ImplementationISPMListView.as_view(),
        name='implementationispm-list'),


    #ImplementationISPMlist showing hidden reports 
    #url(r'^countries/(?P<country>[\w-]+)/eventreportings/hidden/$',
    #    view=EventReportingHiddenListView.as_view(),
    #    name='event-reporting-hidden-list'),

    # ImplementationISPM detail
    url(r'^countries/(?P<country>[\w-]+)/implementationispm/(?P<year>\d+)/(?P<month>\d{2})/(?P<slug>[\w-]+)/$',
        view=ImplementationISPMDetailView.as_view(),
        name="implementationispm-detail"),
        
     #ImplementationISPM create
    url(r'^countries/(?P<country>[\w-]+)/implementationispm/create/$',
        view=implementationispm_create,
        name='implementationispm-create'),
        
    # ImplementationISPM edit
    url(r'^countries/(?P<country>[\w-]+)/implementationispm/edit/(?P<id>\d+)/$',
        view=implementationispm_edit,
        name='implementationispm-edit'),

#-------------------------------------------#

    # pagedown for markdown wysiwyg
    ("^pagedown/", include(mezzanine_pagedown.urls)),
    
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    ("^admin/", include(admin.site.urls)),

    # We don't want to presume how your homepage works, so here are a
    # few patterns you can use to set it up.

    # HOMEPAGE AS STATIC TEMPLATE
    # ---------------------------
    # This pattern simply loads the index.html template. It isn't
    # commented out like the others, so it's the default. You only need
    # one homepage pattern, so if you use a different one, comment this
    # one out.

    url("^$", direct_to_template, {"template": "index.html"}, name="home"),

    # HOMEPAGE AS AN EDITABLE PAGE IN THE PAGE TREE
    # ---------------------------------------------
    # This pattern gives us a normal ``Page`` object, so that your
    # homepage can be managed via the page tree in the admin. If you
    # use this pattern, you'll need to create a page in the page tree,
    # and specify its URL (in the Meta Data section) as "/", which
    # is the value used below in the ``{"slug": "/"}`` part.
    # Also note that the normal rule of adding a custom
    # template per page with the template name using the page's slug
    # doesn't apply here, since we can't have a template called
    # "/.html" - so for this case, the template "pages/index.html"
    # should be used if you want to customize the homepage's template.

    # url("^$", "mezzanine.pages.views.page", {"slug": "/"}, name="home"),

    # HOMEPAGE FOR A BLOG-ONLY SITE
    # -----------------------------
    # This pattern points the homepage to the blog post listing page,
    # and is useful for sites that are primarily blogs. If you use this
    # pattern, you'll also need to set BLOG_SLUG = "" in your
    # ``settings.py`` module, and delete the blog page object from the
    # page tree in the admin if it was installed.

    # url("^$", "mezzanine.blog.views.blog_post_list", name="home"),

    # MEZZANINE'S URLS
    # ----------------
    # ADD YOUR OWN URLPATTERNS *ABOVE* THE LINE BELOW.
    # ``mezzanine.urls`` INCLUDES A *CATCH ALL* PATTERN
    # FOR PAGES, SO URLPATTERNS ADDED BELOW ``mezzanine.urls``
    # WILL NEVER BE MATCHED!

    # If you'd like more granular control over the patterns in
    # ``mezzanine.urls``, go right ahead and take the parts you want
    # from it, and use them directly below instead of using
    # ``mezzanine.urls``.

    ("^", include("mezzanine.urls")),

    # MOUNTING MEZZANINE UNDER A PREFIX
    # ---------------------------------
    # You can also mount all of Mezzanine's urlpatterns under a
    # URL prefix if desired. When doing this, you need to define the
    # ``SITE_PREFIX`` setting, which will contain the prefix. Eg:
    # SITE_PREFIX = "my/site/prefix"
    # For convenience, and to avoid repeating the prefix, use the
    # commented out pattern below (commenting out the one above of course)
    # which will make use of the ``SITE_PREFIX`` setting. Make sure to
    # add the import ``from django.conf import settings`` to the top
    # of this file as well.
    # Note that for any of the various homepage patterns above, you'll
    # need to use the ``SITE_PREFIX`` setting as well.

    # ("^%s/" % settings.SITE_PREFIX, include("mezzanine.urls"))

)





# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
