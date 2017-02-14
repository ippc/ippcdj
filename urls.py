import autocomplete_light
autocomplete_light.autodiscover()

from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.sitemaps import GenericSitemap
from mezzanine.pages.models import RichTextPage
from .news.models import NewsPost

# from django.contrib.auth.decorators import login_required

# from django.contrib.admin.views.decorators import staff_member_required

from django.contrib import admin
admin.autodiscover()
from .ippc.views import IppcUserProfileDetailView,profile_update, PestReportListView, PestReportHiddenListView,\
PestReportDetailView, CountryView,PartnersView, pest_report_create, pest_report_edit, PublicationDetailView,PublicationDetail2View,\
PublicationListView,ReportingObligationListView, ReportingObligationDetailView,reporting_obligation_create, reporting_obligation_edit, \
EventReportingListView, EventReportingDetailView,event_reporting_create, event_reporting_edit,\
PestFreeAreaListView, PestFreeAreaDetailView,pfa_create, pfa_edit,\
WebsiteListView, WebsiteDetailView ,website_create, website_edit, \
ImplementationISPMListView, ImplementationISPMDetailView,implementationispm_create, implementationispm_edit,\
CountryListView,PublicationFilesListView,CountryRelatedView,\
AdvancesSearchCNListView,publication_edit,\
CnPublicationListView,CnPublicationDetailView,country_publication_create,country_publication_edit,\
PartnersPublicationDetailView,  partner_publication_create,  partner_publication_edit,\
PartnersWebsiteDetailView,  partner_websites_create,  partner_websites_edit,\
CountryNewsListView,CountryNewsDetailView,countrynews_create,countrynews_edit,\
CountryNewsListView,CountryNewsDetailView,countrynews_create,countrynews_edit,\
PartnersNewsDetailView,partners_news_create,partners_news_edit,\
PollListView,PollResultsView,PollDetailView,vote_poll,poll_edit,poll_create,\
email_send,EmailUtilityMessageDetailView,EmailUtilityMessageListView,ReminderMessageDetailView,ReminderMessageListView,\
MassEmailUtilityMessageDetailView,MassEmailUtilityMessageListView,massemail_send,massemailutility_to_send,massemailutility_setstatus,\
DraftProtocolDetailView,  draftprotocol_create, draftprotocol_edit,draftprotocol_compilecomments,\
draftprotocol_comment_create,draftprotocol_comment_edit,PublicationLibraryView,commenta,contactPointExtractor,\
CountryRegionsPercentageListView,CountryStatsreportsListView,CountryStatsTotalreportsListView,CountryRegionsUsersListView,CountryTotalUsersListView,CountryStatsChangeInCPsListView,\
CountryRegionsUsersNeverLoggedListView,CountryRegionsUsersNeverLoggedNewListView,CountryStatsTotalreports1ListView,CountryStatsSinglePestReportsListView,CountryStatsSingleReportsListView,CountryStatsTotalReportsIncreaseListView,\
vote_answer_up ,vote_answer_down,reporting_trough_eppo,reminder_to_cn,\
reporting_obligation_validate,event_reporting_validate,pest_report_validate,\
QAQuestionListView, QAQuestionDetailView, QAQuestionAnswersView,question_create,answer_create,\
FAQsListView, faqcategory_edit,faqcategory_create,faq_edit,faq_create,FAQsItemDetailView,FAQsCategoryDetailView,\
ContactUsEmailMessageListView,   ContactUsEmailMessageDetailView , contactus_email_send,UserAutoRegistrationListView,auto_register,auto_register_approve,auto_register_delete,\
IRSSActivityListView,IRSSActivityDetailView,irss_activity_create,irss_activity_edit   ,CountryStatisticsTotalNroByYearListView,subscribe_to_news

#QuestionListView, QuestionDetailView, QuestionAnswersView,question_create,question_edit,answer_edit      
#reporting_obligation_translate,
from schedule.periods import Year, Month, Week, Day
from mezzanine.core.views import direct_to_template

import mezzanine_pagedown.urls

# http://django-envelope.readthedocs.org/en/latest/customization.html
# from envelope.views import ContactView



# Add the urlpatterns for any custom Django applications here.
# You can also change the ``home`` view to add your own functionality
# to the project's homepage.
js_info_dict = {
    'packages': ('ippc',),
}
# Sitemaps 
# Define information to be published in dictionaries
ippcnews_dict = {
    'queryset': NewsPost.objects.published(),
    'date_field': 'publish_date',
    }
page_dict = {
    'queryset': RichTextPage.objects.published(),
    }
sitemaps = {
    'pages': GenericSitemap(page_dict, priority=0.6),
    'ippcnews': GenericSitemap(ippcnews_dict, priority=0.8),
    }


urlpatterns = patterns("",
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
(r'^google10111c8a3426cf77\.html$', lambda r:HttpResponse("google-site-verification: google10111c8a3426cf77.html", mimetype="text/plain")),
(r'^robots\.txt$', lambda r: HttpResponse("User-agent:*\nDisallow: ", mimetype="text/plain")),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
   
   #-------------- NEWS notification subscribe:
   url(r'^news-subscribe/$',subscribe_to_news, name='subscribe_to_news'),
   
  
   #---------IRSS:--------------------------#    
    
    #url("devirss.ippc.int/$', direct_to_template, {"template": "irss/index.html"}, name="irss"),
    #url(r'^irss/$', direct_to_template, {"template": "irss/index.html"}, name="irss"),
   # url(r'^irss/activities_old/$', direct_to_template, {"template": "irss/irss_activities.html"}, name="irss activities"),
    #url(r'^irss/about/$', direct_to_template, {"template": "irss/irss_about.html"}, name="irssabout"),
    #url(r'^irss/country-profiles/$', direct_to_template, {"template": "irss/irss_countries.html"}, name="irsscn"),
    url(r'^irss/helpdesk/$', direct_to_template, {"template": "irss/irss_helpdeskhome.html"}, name="irsshd"),
    #url(r'^irss/helpdesk-1/$', direct_to_template, {"template": "irss/irss_helpdeskhome.html"}, name="irsshelpdesk"),
    #url(r'^irss/helpdesk-faq/$', direct_to_template, {"template": "irss/irss_helpdeskfaq.html"}, name="irssfaq"),
    
    #----------IRSS new activities:------------------------------#    
  
    url(r'^irss/activities/$',  view=IRSSActivityListView.as_view(), name='irss-activities-list'),
    url(r'^irss/activities/(?P<pk>\d+)/$',view=IRSSActivityDetailView.as_view(), name="irss-activity-detail"),
    url(r'^irss/activities/create/$', view=irss_activity_create, name='irss-activity-create'),
    url(r'^irss/activities/edit/(?P<id>\d+)/$', view=irss_activity_edit, name='irss-activity-edit'),
        
     #----------IRSS Q&A:------------------------------#    
  
    url(r'^qa/$',QAQuestionListView.as_view(), name='index'),
    url(r'^qa/(?P<pk>\d+)/$', QAQuestionDetailView.as_view(), name='detail'),
    url(r'^qa/create/$',view=question_create,name='question-create'),
    url(r'^qa/(?P<pk>\d+)/answers/$', QAQuestionAnswersView.as_view(), name='answers'),
    url(r'^qa/(?P<question_id>\d+)/answer/create/$', answer_create, name='answer-create'),
    url(r'^qa/(?P<question_id>\d+)/answer/(?P<id>\d+)/voteup/$', vote_answer_up, name='vote-up'),
    url(r'^qa/(?P<question_id>\d+)/answer/(?P<id>\d+)/votedown/$', vote_answer_down, name='vote-down'),
    
    
#     url(r'^qa/$',QuestionListView.as_view(), name='index'),
#    url(r'^qa/(?P<pk>\d+)/$', QuestionDetailView.as_view(), name='detail'),
#    url(r'^qa/create/$',view=question_create,name='question-create'),
#    url(r'^qa/edit/(?P<id>\d+)/$', view=question_edit, name='question-edit'),
#    url(r'^qa/(?P<pk>\d+)/answers/$', QuestionAnswersView.as_view(), name='answers'),
#    url(r'^qa/(?P<question_id>\d+)/answer/create/$', answer_create, name='answer-create'),
#    url(r'^qa/(?P<question_id>\d+)/answer/(?P<id>\d+)/edit/$', answer_edit, name='answer-edit'),
#    url(r'^qa/(?P<question_id>\d+)/answer/(?P<id>\d+)/voteup/$', vote_answer_up, name='vote-up'),
#    url(r'^qa/(?P<question_id>\d+)/answer/(?P<id>\d+)/votedown/$', vote_answer_down, name='vote-down'),
    
    #---------AUTO-REGISTER-USER ------------------------------#    
    url(r'^accounts/pendingapproval/$',UserAutoRegistrationListView.as_view(), name='index'),
    url(r'^accounts/autoregister/$',view=auto_register,name='auto-register'),
    url(r'^accounts/autoregister/approve/(?P<id>\d+)/$',view=auto_register_approve,name='auto-register-approve'),
    url(r'^accounts/autoregister/delete/(?P<id>\d+)/$',view=auto_register_delete,name='auto-register-delete'),
   
   #---------EPPO REPORTING------------------------------------
    url(r'^epporeporting/', reporting_trough_eppo, name='reporting_trough_eppo'),

    #--------- Reminder system ------------------------------------
    url(r'^reminder/(?P<id>\d+)/$', reminder_to_cn, name='reminder_to_cn'),
    url(r'^remindermessages/all/$',view=ReminderMessageListView.as_view(), name='remindermessages-list'),
    url(r'^remindermessages/(?P<pk>\d+)/$',ReminderMessageDetailView.as_view(), name='remindermessages-detail'),
   #----------------- FAQs DB-------------
   url(r'^faq/$',FAQsListView.as_view(), name='faqlist'),
   url(r'^faq/category/(?P<pk>\d+)/$', FAQsCategoryDetailView.as_view(), name='faqcategory-detail'),
   url(r'^faq/category_create/$',view=faqcategory_create,name='faqcategory-create'),
   url(r'^faq/category_edit/(?P<id>\d+)/$', view=faqcategory_edit, name='faqcategory-edit'),
   url(r'^faq/(?P<pk>\d+)/$', FAQsItemDetailView.as_view(), name='faq-detail'),
   url(r'^faq/create/$',view=faq_create,name='faq-create'),
   url(r'^faq/edit/(?P<id>\d+)/$', view=faq_edit, name='faq-edit'),

   #--------------------------------------
    url(r'^forum/', include('forum.urls')),
    url(r'^calls/', include('calls.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^iyph/', include('iyph.urls')),
    url(r'^pce/', include('pce.urls')),



    url('^markdown/', include( 'django_markdown.urls')),
    # forum detail
    # url(r'^forum/(?P<slug>[\w-]+)/$',
    #     view=ForumPostDetailView.as_view(),
    #     name="forum-post-detail"),
    # url(r'^contact/',    include('envelope.urls')),
    # url(r'^contact/', ContactView.as_view(
    #     template_name="envelope/contact_form.html",
    #     success_url="/thankyou/",
    # )),
    url("^sitemap/$", direct_to_template, {"template": "sitemap.html"}, name="sitemap"),
    #url("^contact/$", direct_to_template, {"template": "contact.html"}, name="contact"),
    url("^thankyou/$", direct_to_template, {"template": "thankyou.html"}, name="thankyou"),
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
    url(r'^countries/(?P<country>[\w-]+)/calendar/$',
        'schedule.views.calendar_by_cn',
        name="country_calendar",
        kwargs={'template_name': 'schedule/calendar_cn.html'}),
        
        
    url(r'^countries/(?P<country>[\w-]+)/(?P<calendar_slug>[-\w]+)/add/$',
        'schedule.views.create_or_edit_event',
        name='calendar_create_event'),
    url(r'^create/(?P<country>[\w-]+)/(?P<calendar_slug>[-\w]+)/$',
        'schedule.views.create_or_edit_event',
        name='calendar_create_event'),   
    #edit    
    url(r'^edit/(?P<country>[\w-]+)/(?P<calendar_slug>[-\w]+)/(?P<event_id>\d+)/$',
        'schedule.views.create_or_edit_event',
        name='edit_event'),    
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
    
    url(r'^countries/all/(?P<type>[\w-]+)/$',
        view=AdvancesSearchCNListView.as_view(),
        name='advsearch'),
     url(r'^countriescontacts/extractor/$',
        view=contactPointExtractor,
        name='contactextractor'),
        
    
    #-------------------STATS------------------------    
   
    url(r'^countries/statistics/regionspercentage/$',view=CountryRegionsPercentageListView.as_view(), name='regionspercentage'),   
   
    url(r'^countries/statistics/reports/$',        view=CountryStatsreportsListView.as_view(), name='statsreports'),
    url(r'^countries/statistics/total-reports/$', view=CountryStatsTotalreportsListView.as_view(),   name='statstotalreports'),  
    url(r'^countries/statistics/region-users/$',    view=CountryRegionsUsersListView.as_view(),  name='regionusers'),
    url(r'^countries/statistics/total-users/$',  view=CountryTotalUsersListView.as_view(),  name='totalusers'),
        
    #url(r'^countries/statistics/region-users-neverlogged/$',
    #    view=CountryRegionsUsersNeverLoggedListView.as_view(),
    #    name='regionusers'),    
    url(r'^countries/statistics/totalnrobyyear/(?P<year>\d+)/$',  view=CountryStatisticsTotalNroByYearListView.as_view(),   name='totalnrobyyear'),
    url(r'^countries/statistics/totalnrobyyear/$',  view=CountryStatisticsTotalNroByYearListView.as_view(),   name='totalnrobyyear'),
   
    
    url(r'^countries/statistics/region-users-neverlogged/(?P<year>\d+)/$',    view=CountryRegionsUsersNeverLoggedNewListView.as_view(),       name='neverlogged'),  ###  
    url(r'^countries/statistics/region-users-neverlogged/$',    view=CountryRegionsUsersNeverLoggedNewListView.as_view(),       name='neverlogged'),    ####
    
    
    url(r'^countries/statistics/total-reports1/(?P<year>\d+)/$',      view=CountryStatsTotalreports1ListView.as_view(),     name='regionusers'),###
    url(r'^countries/statistics/total-reports1/$',      view=CountryStatsTotalreports1ListView.as_view(),     name='regionusers'),###
    
    url(r'^countries/statistics/totalreporting-increase/(?P<year>\d+)/$',     view=CountryStatsTotalReportsIncreaseListView.as_view(),     name='regionusers'),###
    url(r'^countries/statistics/totalreporting-increase/$',     view=CountryStatsTotalReportsIncreaseListView.as_view(),     name='regionusers'),###
  
    url(r'^countries/statistics/change-in-cp/(?P<year>\d+)/$',   view=CountryStatsChangeInCPsListView.as_view(),   name='regionusers'), ###  
    url(r'^countries/statistics/change-in-cp/$',   view=CountryStatsChangeInCPsListView.as_view(),   name='regionusers'),   ###
    url(r'^countries/statistics/singlereporting/(?P<year>\d+)/$',    view=CountryStatsSingleReportsListView.as_view(), name='regionspercentage'),   ##
    url(r'^countries/statistics/singlereporting/$',    view=CountryStatsSingleReportsListView.as_view(), name='regionspercentage'),   ##
   
    url(r'^countries/statistics/year-pestreports/(?P<year>\d+)/$',    view=CountryStatsSinglePestReportsListView.as_view(), name='regionspercentage'),   ##
    url(r'^countries/statistics/year-pestreports/$',    view=CountryStatsSinglePestReportsListView.as_view(), name='regionspercentage'),   ##
   
    #-------------------------------------------#    
    #POLL:
    
    url(r'^poll/$',PollListView.as_view(), name='index'),
    url(r'^poll/(?P<pk>\d+)/$', PollDetailView.as_view(), name='detail'),
    url(r'^poll/(?P<pk>\d+)/results/$', PollResultsView.as_view(), name='results'),
    url(r'^poll/(?P<poll_id>\d+)/vote/$', vote_poll, name='vote'),
    url(r'^poll/create/$',
        view=poll_create,
        name='poll-create'),
    
    url(r'^poll/edit/(?P<id>\d+)/$',
        view=poll_edit,
        name='poll-edit'),
    
    
    
    
    #--------------------------------------#
    #EMAIL:
    
#    url(r'^emailutility/$',PollListView.as_view(), name='index'),
#    url(r'^poll/(?P<pk>\d+)/$', PollDetailView.as_view(), name='detail'),
#    url(r'^poll/(?P<pk>\d+)/results/$', PollResultsView.as_view(), name='results'),
#    url(r'^poll/(?P<poll_id>\d+)/send/$', vote_poll, name='vote'),
    url(r'^emailutility/all/$',
        view=EmailUtilityMessageListView.as_view(),
        name='email-list'),
    url(r'^emailutility/(?P<pk>\d+)/$',EmailUtilityMessageDetailView.as_view(), name='email-detail'),
    url(r'^emailutility/send/$',
        view=email_send,
        name='email-send'),
    #--------------------------------------#
    # MASS EMAIL:    
    url(r'^massemailutility/all/$',view=MassEmailUtilityMessageListView.as_view(), name='mass-email-list'),
    url(r'^massemailutility/(?P<pk>\d+)/$',MassEmailUtilityMessageDetailView.as_view(), name='mass-email-detail'),
    url(r'^massemailutility/send/$',view=massemail_send, name='mass-email-send'),
    url(r'^massemailutility/status/(?P<pk>\d+)/(?P<status>\d+)/$',view=massemailutility_setstatus, name='mass-email-status'),
    url(r'^massemailutility_to_send/sendout/$', massemailutility_to_send, name='massemailutility-to-send'),
     
    #------- CONTACT US EMAIL--------------------------------------#
    url(r'^contactusemail/all/$', view=ContactUsEmailMessageListView.as_view(),  name='contactus-email-list'),
    url(r'^contactusemail/(?P<pk>\d+)/$',ContactUsEmailMessageDetailView.as_view(), name='contactus-email-detail'),
    url(r'^contact/$',  view=contactus_email_send,    name='contactus-email-send'),    
#   url(r'^contactusemail/send/$',  view=contactus_email_send,    name='contactus-email-send'),    
# --------------------------------------#
   url(r'^countries/(?P<country>[\w-]+)/relatedinformations/$',
        view=CountryRelatedView.as_view(),
        name='related-info'), 
     #--------------------------------------#    
    url(r'^countries/(?P<country>[\w-]+)/pestreports/$',
        view=PestReportListView.as_view(),
        name='pest-report-list'),
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
    url(r'^countries/(?P<country>[\w-]+)/pestreports/validate/(?P<id>\d+)/$',
        view=pest_report_validate,
        name='pest-report-validate'),
#        
        
    # publication list
    url(r'^publications/$',
        view=PublicationListView.as_view(),
        name='publication-list'),

   # publication detail
    url(r'^publications/(?P<pk>\d+)/$',
        view=PublicationDetailView.as_view(),
        name='publication-detail'),
    
    url(r'^publications/(?P<slug>[\w-]+)/$',
        view=PublicationDetail2View.as_view(),
        name='publication-detail'),   
    # work-area publication detail    
    url(r'^work-area-publications/(?P<pk>\d+)/$',
        view=PublicationDetailView.as_view(),
        name='publication-r-detail'),    
    url(r'^work-area-publications/(?P<slug>[\w-]+)/$',
        view=PublicationDetail2View.as_view(),
        name='publication-r-detail'),     
    #-------------------------------------------#
  # publication list files
    url(r'^publications/(?P<id>\d+)/files/$',
        view=PublicationFilesListView.as_view(),
        name='publication-file-list'),

    #-------------------------------------------#
    
    # reporting obligation list
    url(r'^countries/(?P<country>[\w-]+)/reportingobligation/(?P<type>[\w-]+)$',
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
    url(r'^countries/(?P<country>[\w-]+)/reportingobligation/validate/(?P<id>\d+)/$',
        view=reporting_obligation_validate,
        name='reporting-obligation-validate'),
#    url(r'^countries/(?P<country>[\w-]+)/reportingobligation/translate/(?P<lang>[\w-]+)/(?P<id>\d+)/$',
#        view=reporting_obligation_translate,
#        name='reporting-obligation-translate'),    
#    
            
    #-------------------------------------------#
    # event reporting list
    url(r'^countries/(?P<country>[\w-]+)/eventreporting/(?P<type>[\w-]+)$',
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
    url(r'^countries/(?P<country>[\w-]+)/eventreporting/validate/(?P<id>\d+)/$',
        view=event_reporting_validate,
        name='event-reporting-validate'),
#        

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

#-------------PARTNERS---------------------------

    url(r'^partners/international-organizations/(?P<partner>[\w-]+)/$',
        view=PartnersView.as_view(),
        name='partner'),
    url(r'^partners/regional-plant-protection-organizations/(?P<partner>[\w-]+)/$',
        view=PartnersView.as_view(),
        name='partner'), 
    url(r'^liason/organizations/(?P<partner>[\w-]+)/$',
        view=PartnersView.as_view(),
        name='partner'),     

    # partners publications detail
    url(r'^partners/(?P<partners>[\w-]+)/publications/(?P<year>\d+)/(?P<month>\d{2})/(?P<slug>[\w-]+)/$',
        view=PartnersPublicationDetailView.as_view(),
        name="partner-publication-detail"),
     #partners publications create
    url(r'^partners/(?P<partners>[\w-]+)/publications/create/$',
        view=partner_publication_create,
        name='partner-publication-create'),
    # partners publications edit
    url(r'^partners/(?P<partners>[\w-]+)/publications/edit/(?P<id>\d+)/$',
        view=partner_publication_edit,
        name='partner-publication-edit'),
    
    # partners websites detail
    url(r'^partners/(?P<partners>[\w-]+)/websites/(?P<year>\d+)/(?P<month>\d{2})/(?P<slug>[\w-]+)/$',
        view=PartnersWebsiteDetailView.as_view(),
        name="partner-websites-detail"),
     #partners websites create
    url(r'^partners/(?P<partners>[\w-]+)/websites/create/$',
        view=partner_websites_create,
        name='partner-websites-create'),
    # partners websites edit
    url(r'^partners/(?P<partners>[\w-]+)/websites/edit/(?P<id>\d+)/$',
        view=partner_websites_edit,
        name='partner-websites-edit'),
        
   # partners news detail
    url(r'^partners/(?P<partners>[\w-]+)/news/(?P<year>\d+)/(?P<month>\d{2})/(?P<slug>[\w-]+)/$',
        view=PartnersNewsDetailView.as_view(),
        name="partner-news-detail"),
     #partners news create
    url(r'^partners/(?P<partners>[\w-]+)/news/create/$',
        view=partners_news_create,
        name='partner-news-create'),
    # partners news edit
    url(r'^partners/(?P<partners>[\w-]+)/news/edit/(?P<id>\d+)/$',
        view=partners_news_edit,
        name='partner-news-edit'),
             
        
      #-------------DPs---------------------------

    
    # DPs  detail
    #https://www.ippc.int/en/core-activities/expert-consultation-draft-diagnostic-protocols/
    #   url(r'^expert-consultation-on-draft-diagnostic-protocols-ecdp/(?P<year>\d+)/(?P<month>\d{2})/(?P<slug>[\w-]+)/$',
    url(r'^core-activities/expert-consultation-draft-diagnostic-protocols/(?P<year>\d+)/(?P<month>\d{2})/(?P<slug>[\w-]+)/$',
        view=DraftProtocolDetailView.as_view(),
        name="draftprotocol-detail"),
     #DPs create
    url(r'^draftprotocol/create/$',
        view=draftprotocol_create,
        name='draftprotocol-create'),
     #   DPsedit
    url(r'^draftprotocol/edit/(?P<id>\d+)/$',
        view=draftprotocol_edit,
        name='draftprotocol-edit'),
    url(r'^draftprotocol/compile/(?P<id>\d+)/$',
        view=draftprotocol_compilecomments,
        name='draftprotocol_compilecomments'),
        
    # individual country home
    #url(r'^expert-consultation-on-draft-diagnostic-protocols-ecdp/$',
    url(r'^core-activities/expert-consultation-draft-diagnostic-protocols/$',
        view=PublicationLibraryView.as_view(),
        # view=country_view(),
        name='country'),
    url(r'^about/secretariat/$',
        view=PublicationLibraryView.as_view(),
        # view=country_view(),
        name='country'),
    url(r'^core-activities/standards-setting/standards-committee/$',
        view=PublicationLibraryView.as_view(),
        # view=country_view(),
        name='country'),
    url(r'^core-activities/standards-setting/expert-drafting-groups/technical-panels/technical-panel-diagnostic-protocols/$',
        view=PublicationLibraryView.as_view(),
        # view=country_view(),
        name='country'),
    url(r'^ephyto/ephyto-steering-group/$',
        view=PublicationLibraryView.as_view(),
        # view=country_view(),
        name='country'),    
        
    url(r'^core-activities/standards-setting/expert-drafting-groups/technical-panels/technical-panel-forest-quarantine/$',
        view=PublicationLibraryView.as_view(),
        # view=country_view(),
        name='country'),
        
    url(r'^core-activities/standards-setting/expert-drafting-groups/technical-panels/technical-panel-phytosanitary-treatments/$',
        view=PublicationLibraryView.as_view(),
        # view=country_view(),
        name='country'),
    url(r'^core-activities/standards-setting/expert-drafting-groups/technical-panels/technical-panel-glossary-phytosanitary-terms-ispm-5/$',
        view=PublicationLibraryView.as_view(),
        # view=country_view(),
        name='country'),
    url(r'^core-activities/standards-setting/expert-drafting-groups/technical-panels/technical-panel-fruit-flies/$',
        view=PublicationLibraryView.as_view(),
        # view=country_view(),
        name='country'),
    url(r'^core-activities/governance/bureau/$',
        view=PublicationLibraryView.as_view(),
        # view=country_view(),
        name='country'),
    url(r'^work-area-pages/standards-committee/electronic-decisions-by-sc/$',
        view=PublicationLibraryView.as_view(),
        # view=country_view(),
        name='country'),
            
        
 
    #-------------DPs Comments---------------------------

    
  
     #DPs Comments create
    url(r'^draftprotocolcomments/create/(?P<id>\d+)/$',
        view=draftprotocol_comment_create,
        name='draftprotocol-comment-create'),
     # DPs Comments DPsedit
     url(r'^draftprotocolcomments/edit/(?P<dp_id>\d+)/(?P<id>\d+)/$',
        view=draftprotocol_comment_edit,
        name='draftprotocol-comment-edit'),

        
#-------------------------------------------#
    # CN news list
    url(r'^countries/(?P<country>[\w-]+)/countrynews/$',
        view=CountryNewsListView.as_view(),
        name='country-news-list'),

    #CN news list showing hidden reports 
    #url(r'^countries/(?P<country>[\w-]+)/countrynews/hidden/$',
    #    view=CountryNewsListView.as_view(),
    #    name='country-news-hidden-list'),

    # CN publications detail
    url(r'^countries/(?P<country>[\w-]+)/countrynews/(?P<year>\d+)/(?P<month>\d{2})/(?P<slug>[\w-]+)/$',
        view=CountryNewsDetailView.as_view(),
        name="country-news-detail"),
        
     # CN publications create
    url(r'^countries/(?P<country>[\w-]+)/countrynews/create/$',
        view=countrynews_create,
        name='country-news-create'),
        
    # CN publications edit
    url(r'^countries/(?P<country>[\w-]+)/countrynews/edit/(?P<id>\d+)/$',
        view=countrynews_edit,
        name='country-news-edit'),
    # event reporting list showing hidden reports 
    #url(r'^countries/(?P<country>[\w-]+)/eventreporting/hidden/$',
    #    view=EventReportingHiddenListView.as_view(),
    #    name='event-reporting-hidden-list'),
    #------------------USERS------------------
    #url(r'^users/(?P<pk>[\w-]+)/$',
    #    view=IppcUserProfileDetailView.as_view(),
    #    name="user-detail"),
    # url(r'^account/update/(?P<id>[\w-]+)/$',
    #     view=profile_update,
    #     name="profile-update"),
         
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

#-----------PUBLICATION-------------------#
   url(r'^publication/edit/(?P<id>\d+)/$',
        view=publication_edit,
        name='publication-edit'),

# forum comments? boh! https://github.com/ippc/ippcdj/commit/184131f38d4a7e24bcbe3fa7b2be97ae0c321a5d#diff-de6dd4b4c889fe0882cfd3f6df5aa451R531 
    url(r'^comment/$',
        view=commenta,
        name='commenta'),


    url(r"^login/user/(?P<user_id>.+)/$", "loginas.views.user_login", name="loginas-user-login"),


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
