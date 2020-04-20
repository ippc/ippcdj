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
PartnersWebsiteDetailView,  partner_websites_create,  partner_websites_edit,partner_page_edit,\
CountryNewsListView,CountryNewsDetailView,countrynews_create,countrynews_edit,\
CountryNewsListView,CountryNewsDetailView,countrynews_create,countrynews_edit,\
PartnersNewsDetailView,partners_news_create,partners_news_edit,\
PollListView,PollResultsView,PollDetailView,vote_poll,poll_edit,poll_create,\
email_send,EmailUtilityMessageDetailView,EmailUtilityMessageListView,ReminderMessageDetailView,ReminderMessageListView,\
MassEmailUtilityMessageDetailView,MassEmailUtilityMessageListView,massemail_send,massemailutility_to_send,massemailutility_setstatus,mergemassemail_send,\
DraftProtocolDetailView,  draftprotocol_create, draftprotocol_edit,draftprotocol_compilecomments,\
draftprotocol_comment_create,draftprotocol_comment_edit,PublicationLibraryView,commenta,contactPointExtractor,\
CountryRegionsPercentageListView,CountryStatsreportsListView,CountryStatsTotalreportsListView,CountryRegionsUsersListView,CountryTotalUsersListView,CountryStatsChangeInCPsListView,\
CountryRegionsUsersNeverLoggedListView,CountryRegionsUsersNeverLoggedNewListView,CountryStatsTotalreports1ListView,CountryStatsSinglePestReportsListView,CountryStatsNROsDetailView,CountryStatsSingleReportsListView,CountryStatsTotalReportsIncreaseListView,\
vote_answer_up ,vote_answer_down,reporting_trough_eppo,reporting_trough_eppo1,reminder_to_cn,\
reporting_obligation_validate,event_reporting_validate,pest_report_validate,\
QAQuestionListView, QAQuestionDetailView, QAQuestionAnswersView,question_create,answer_create,\
FAQsListView, faqcategory_edit,faqcategory_create,faq_edit,faq_create,FAQsItemDetailView,FAQsCategoryDetailView,\
ContactUsEmailMessageListView,   ContactUsEmailMessageDetailView , contactus_email_send,UserAutoRegistrationListView,auto_register,auto_register_approve,auto_register_delete,\
IRSSActivityListView,IRSSActivityDetailView,irss_activity_create,irss_activity_edit   ,CountryStatisticsTotalNroByYearListView,subscribe_to_news,unsubscribe_to_news,NewsStatisticsByYearListView,\
UserMembershipHistoryListView,UserMembershipHistoryDetailView,usermembershiphistory_create,usermembershiphistory_edit,MediaKitDocumentListView,CountryStatsSingleLegislationsListView,\
PhytosanitaryTreatmentDetailView,PhytosanitaryTreatmentListView ,phytosanitarytreatment_create,phytosanitarytreatment_edit,\
CertificatesToolListView,CertificatesToolDetailView,generate_certificates,MembershipListView,generate_list,generate_replacementlist,generate_listNEW,\
TopicDetailView,TopicListView,topic_create,topic_edit,topic_translate,WorkshopCertificatesToolListView,WorkshopCertificatesToolDetailView,generate_workshopcertificates,\
B_CertificatesToolListView,B_CertificatesToolDetailView,generate_b_certificates,my_tool,MyToolDetailView,generate_topiclist,\
MembershipShortListView,generate_shortlist,generate_shortlistparticipant,generate_listNEW1,\
generate_b_certificatesnew,generate_certificatesnew,CountryStatsSingleListOfRegulatesPestsListView,select_cns_nros_stats,nro_stats_files,contactPointsXML,\
ContributedResourceListView,  ContributedResourceDetailView,ContributedResourcePendingListView,ContributedResourcePendingDetailView,contribuitedresource_create,contribuitedresource_edit,my_tool2,MyTool2DetailView,nro_stats3_files,AdvancesSearchResourcesListView,PublicationMeetingFilesListView,ReportingSystemCNListView,\
ReportingSystemSummaryCNListView,UserAutoRegistrationResourcesListView,auto_registerresources,auto_registerresources_approve,auto_registerresources_delete
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
   url(r'^news-subscribe/(?P<type>\d+)/$',subscribe_to_news, name='subscribe_to_news'),
   url(r'^news-un-subscribe/(?P<type>\d+)/$',unsubscribe_to_news, name='un-subscribe_to_news'),
   
  
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
 #---------AUTO-REGISTER-USER RESOURCES------------------------------#    
    url(r'^contributed-resource/accounts/pendingapprovalresources/$',UserAutoRegistrationResourcesListView.as_view(), name='index'),
    url(r'^contributed-resource/accounts/autoregisterresources/$',view=auto_registerresources,name='auto-registerresources'),
    url(r'^contributed-resource/accounts/autoregisterresources/approve/(?P<id>\d+)/$',view=auto_registerresources_approve,name='auto-registerresources-approve'),
    url(r'^contributed-resource/accounts/autoregisterresources/delete/(?P<id>\d+)/$',view=auto_registerresources_delete,name='auto-registerresources-delete'),
 
   #---------EPPO REPORTING------------------------------------
    url(r'^epporeporting/', reporting_trough_eppo, name='reporting_trough_eppo'),
    url(r'^epporeporting1/', reporting_trough_eppo1, name='reporting_trough_eppo1'),

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
    url(r'^ph/', include('iyph.urls')),
    url(r'^pce/', include('pce.urls')),
    #PHYTO#
    #url(r'^phytosanitary/', include('phytosanitary.urls')),
    url(r'^e-learning/', include('learn.urls')),
    


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
    url("^organigram_a/$", direct_to_template, {"template": "organigram_a.html"}, name="organigram_a"),
    url("^organigram_b/$", direct_to_template, {"template": "organigram_b.html"}, name="organigram_b"),
    url("^organigram_c/$", direct_to_template, {"template": "organigram_c.html"}, name="organigram_c"),
  
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
    
    #register-to-event
      url(r'^register/(?P<id>\d+)/$',
        'schedule.views.register_to_event',
        name='register-to-event'),   
    #un-register-to-event
      url(r'^un-register/(?P<id>\d+)/$',
        'schedule.views.unregister_to_event',
        name='un-register-to-event'), 
    #url(r'^generate-participants-list/(?P<id>\d+)/$',
    #    'ippc.views.generate_participantslist',
    #    name='generate-participants-list'),     
   url(r'^resend-invite/(?P<id>\d+)/$',
        'schedule.views.resend_invite',
        name='resend-invite'),     
    
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
    url(r'^countriescontacts/cp/$',
        view=contactPointsXML,
        name='countriescontacts'),
     url(r'^countries/reportingsystem/(?P<type>[\w-]+)/(?P<year>\d+)/(?P<month>\d{2})/$',
        view=ReportingSystemCNListView.as_view(),
        name='reportingsystem'),    
     url(r'^countries/reportingsystem-summary/(?P<type>[\w-]+)/$',
        view=ReportingSystemSummaryCNListView.as_view(),
        name='reportingsystem'),    
    #----- CAP DEV RES
    url(r'^resources/capacity-development-resources/resources-by-topic/(?P<type>[\w-]+)/$',
        view=AdvancesSearchResourcesListView.as_view(),
        name='advsearch'),
    #-------------------NEWS STATS------------------------    
   
    url(r'^resources/statistics/news-statistics/$',view=NewsStatisticsByYearListView.as_view(), name='newsstatistics'),   
    url(r'^resources/statistics/news-statistics/(?P<year>\d+)/$',  view=NewsStatisticsByYearListView.as_view(),   name='newsstatistics'),
   
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
    url(r'^countries/statistics/year-legislations/(?P<year>\d+)/$',    view=CountryStatsSingleLegislationsListView.as_view(), name='regionspercentage'),   ##
    url(r'^countries/statistics/year-legislations/$',    view=CountryStatsSingleLegislationsListView.as_view(), name='regionspercentage'),   ##
    url(r'^countries/statistics/year-regulatedpests/$',    view= CountryStatsSingleListOfRegulatesPestsListView.as_view(), name='regionspercentage'),   ##
    #url(r'^countries/statistics/nros-by-countries/$',    view= CountryStatsNROsListView.as_view(), name='regionspercentage'),   ##
    url(r'^countries/statistics/createnrostats/$',view=select_cns_nros_stats, name='select_cns_nros_stats'),
    url(r'^countries/statistics/(?P<pk>\d+)/$',CountryStatsNROsDetailView.as_view(), name='nro-stats-detail'),
  
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
    # CERTIFICATES:    
    url(r'^work-area/certificatestool/all/$',view=CertificatesToolListView.as_view(), name='certificatestool-list'),
    url(r'^work-area/certificatestool/(?P<pk>\d+)/$',CertificatesToolDetailView.as_view(), name='certificatestool-detail'),
    url(r'^work-area/certificatestool/create/$',view=generate_certificates, name='certificatestool-create'),
    url(r'^work-area/certificatestoolnew/create/$',view=generate_certificatesnew, name='certificatestoolnew-create'),
    #--------------------------------------#
    # Workshop CERTIFICATES:    
    url(r'^work-area/w-certificatestool/all/$',view=WorkshopCertificatesToolListView.as_view(), name='w-certificatestool-list'),
    url(r'^work-area/w-certificatestool/(?P<pk>\d+)/$',WorkshopCertificatesToolDetailView.as_view(), name='w-certificatestool-detail'),
    url(r'^work-area/w-certificatestool/create/$',view=generate_workshopcertificates, name='w-certificatestool-create'),
   #--------------------------------------#
    # bureau/cpm CERTIFICATES:    
    url(r'^work-area/b-certificatestool/all/$',view=B_CertificatesToolListView.as_view(), name='b-certificatestool-list'),
    url(r'^work-area/b-certificatestool/(?P<pk>\d+)/$',B_CertificatesToolDetailView.as_view(), name='b-certificatestool-detail'),
    url(r'^work-area/b-certificatestool/create/$',view=generate_b_certificates, name='b-certificatestool-create'),
    url(r'^work-area/b-certificatestoolnew/create/$',view=generate_b_certificatesnew, name='b-certificatestoolnew-create'),
    
    #MEMBERSHIT LIST TOOL
    url(r'^work-area/membershiptool/$',      view=MembershipListView.as_view(),     name='membership-list'),###
    #url(r'^work-area/membershiptool/(?P<type>[\w-]+)/create/(?P<id>\d+)/$',      view=generate_list,     name='generate-list'),###
    url(r'^work-area/membershiptool/create/(?P<id>\d+)/$',      view=generate_listNEW1,     name='generate-list'),###
    url(r'^work-area/membershiplisttool/create/(?P<id>\d+)/$',      view=generate_listNEW,     name='generate-listnew'),###
    
    url(r'^generate-participants-list/(?P<type>\d+)/(?P<id>\d+)/$' , view=generate_list,   name='generate-list'),    
    #SHORT LIST
    url(r'^work-area/membershipshorttool/$', view=MembershipShortListView.as_view(),     name='membership-shortlist'),###paoalnew
    url(r'^work-area/membershiptoolshort/(?P<type>[\w-]+)/create/(?P<id>\d+)/$',      view=generate_shortlist,     name='generate-shortlist'),###
    url(r'^work-area/participantshortlist/(?P<id>\d+)/create/$',      view=generate_shortlistparticipant,     name='generate-shortlistparticipant'),###
    url(r'^generate-participants-shortlist/(?P<type>\d+)/(?P<id>\d+)/$' , view=generate_shortlist,   name='generate-shortlist'),    
    
    #url(r'^generate-participants-list/(?P<id>\d+)/$','ippc.views.generate_participantslist',  name='generate-participants-list'),    
    #url(r'^work-area/sss/(?P<id>\d+)/$',      view=generate_membershiplist,     name='generate_membershiplist'),###
    url(r'^work-area/mytool/$',view= my_tool , name='my_tool'),
    url(r'^work-area/mytoolres/(?P<pk>\d+)/$',view= MyToolDetailView.as_view() , name='my_toolres'),
    url(r'^work-area/mytool2/$',view= my_tool2 , name='my_tool2'),
    url(r'^work-area/mytool2res/(?P<pk>\d+)/$',view= MyTool2DetailView.as_view() , name='my_tool2res'),
    url(r'^work-area/nro_stats_files/$',view= nro_stats_files , name='nro_stats_files'),
    url(r'^work-area/nro_stats3_files/$',view= nro_stats3_files , name='nro_stats3_files'),
   
  
    # url(r'^aaa/pdf/$', view=CertificatePDFView.as_view(), name='aaa-pdf'),
    
    #--------------------------------------#
    #EMAIL:
    
#    url(r'^emailutility/$',PollListView.as_view(), name='index'),
#    url(r'^poll/(?P<pk>\d+)/$', PollDetailView.as_view(), name='detail'),
#    url(r'^poll/(?P<pk>\d+)/results/$', PollResultsView.as_view(), name='results'),
#    url(r'^poll/(?P<poll_id>\d+)/send/$', vote_poll, name='vote'),
    # MERGE EMAIL:    
    url(r'^mergemassemailutility/send/$',view=mergemassemail_send, name='mass-email-send'),
       #--------------------------------------#
    
    url(r'^emailutility/all/$',
        view=EmailUtilityMessageListView.as_view(),
        name='email-list'),
    url(r'^emailutility/(?P<pk>\d+)/$',EmailUtilityMessageDetailView.as_view(), name='email-detail'),
    url(r'^emailutility/send/$',        view=email_send,        name='email-send'),
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
    url(r'^publicationslist/$',
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
# publication list files
    url(r'^publications-meetings/(?P<id>\d+)/files/$',
        view=PublicationMeetingFilesListView.as_view(),
        name='publication-meetings-file-list'),

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

#    url(r'^partners/international-organizations/(?P<partner>[\w-]+)/$',
#        view=PartnersView.as_view(),
#        name='partner'),
#    url(r'^partners/regional-plant-protection-organizations/(?P<partner>[\w-]+)/$',
#        view=PartnersView.as_view(),
#        name='partner'), 
#    url(r'^liason/organizations/(?P<partner>[\w-]+)/$',
#        view=PartnersView.as_view(),
#        name='partner'),     
url(r'^external-cooperation/organizations-page-in-ipp/(?P<partner>[\w-]+)/$',        view=PartnersView.as_view(),        name='partner'),
    url(r'^external-cooperation/regional-plant-protection-organizations/(?P<partner>[\w-]+)/$',        view=PartnersView.as_view(),        name='partner'), 
   # url(r'^liason/organizations/(?P<partner>[\w-]+)/$',        view=PartnersView.as_view(),        name='partner'),     
 

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
             
        url(r'^partners/page/edit/(?P<id>\d+)/$',
        view=partner_page_edit,
        name='partner-page-edit'),
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
    url(r'^work-area-pages/capacity-development/implementation-and-capacity-development-committee-ic/electronic-decisions-by-ic/$',
           view=PublicationLibraryView.as_view(),
           # view=country_view(),
           name='country'),     
    ##    url(r'^core-activities/external-cooperation/$',
    ##    view=PublicationLibraryView.as_view(),
    ##    # view=country_view(),
    ##    name='country'),        
        
 
    #-------------DPs Comments---------------------------

    
  
     #DPs Comments create
    url(r'^draftprotocolcomments/create/(?P<id>\d+)/$',
        view=draftprotocol_comment_create,
        name='draftprotocol-comment-create'),
     # DPs Comments DPsedit
     url(r'^draftprotocolcomments/edit/(?P<dp_id>\d+)/(?P<id>\d+)/$',
        view=draftprotocol_comment_edit,
        name='draftprotocol-comment-edit'),
#--------------------------------

#------------ PHYTO TREATMENT----------------------
    url(r'^core-activities/standards-setting/technical-panels/technical-panel-phytosanitary-treatments/phytosanitary-treatments-tool/(?P<slug>[\w-]+)/$',
        view=PhytosanitaryTreatmentDetailView.as_view(), name="phytosanitary-treatment-detail"),
     #create
    url(r'^core-activities/standards-setting/technical-panels/technical-panel-phytosanitary-treatments/phytosanitary-treatments-tool/create/new/$',
        view=phytosanitarytreatment_create,
        name='phytosanitary-treatment-create'),
     #   edit
        url(r'^core-activities/standards-setting/technical-panels/technical-panel-phytosanitary-treatments/phytosanitary-treatments-tool/edit/(?P<id>\d+)/$',
        view=phytosanitarytreatment_edit,
        name='phytosanitary-treatment-edit'),
    url(r'^core-activities/standards-setting/technical-panels/technical-panel-phytosanitary-treatments/phytosanitary-treatments-tool/$',
        view=PhytosanitaryTreatmentListView.as_view(),
        # view=country_view(),
        name='phytosanitary-treatment-list'),
#------------ LIST of  Topics ----------------------
    url(r'^core-activities/standards-setting/list-topics-ippc-standards/(?P<slug>[\w-]+)/$',
        view=TopicDetailView.as_view(), name="topic-detail"),
     #create
    url(r'^core-activities/standards-setting/list-topics-ippc-standards/topic/create/new/$',
        view=topic_create,
        name='topic-create'),
     #   edit
        url(r'^core-activities/standards-setting/list-topics-ippc-standards/topic/edit/(?P<id>\d+)/$',
        view=topic_edit,
        name='topic-edit'),
    url(r'^core-activities/standards-setting/list-topics-ippc-standards/list$',
        view=TopicListView.as_view(),
        name='topic-list'),
        url(r'^core-activities/standards-setting/list-topics-ippc-standards/topic/translate/(?P<lang>[\w-]+)/(?P<id>\d+)/$',
        view=topic_translate,
        name='topic-translate'),    
  url(r'^work-area/generate-lot/(?P<lang>[\w-]+)$',      view=generate_topiclist,     name='generate-topiclist'),###
  
  url(r'^work-area/generate-sc-shortlist/$',view=generate_shortlist, name='generate-sc-shortlist'),
  url(r'^work-area/generate-sc-replacementlist/$',view=generate_replacementlist, name='generate-sc-replacementlist'),
   #----------------------------------------#
   #------- CONTRIBUTED RESOURCES------------------#
    url(r'^core-activities/capacity-development/guides-and-training-materials/contributed-resource-list/$',
        view=ContributedResourceListView.as_view(),        name='contributed-resource-list'),
    url(r'^core-activities/capacity-development/guides-and-training-materials/contributed-resource-detail/(?P<slug>[\w-]+)/$',
        view=ContributedResourceDetailView.as_view(), name="contributed-resource-detail"),
    url(r'^core-activities/capacity-development/guides-and-training-materials/contributed-resource-list/pending/$',
        view=ContributedResourcePendingListView.as_view(),        name='contributed-resource-pending-list'),
    url(r'^core-activities/capacity-development/guides-and-training-materials/contributed-resource-detail/pending/(?P<slug>[\w-]+)/$',
        view=ContributedResourcePendingDetailView.as_view(), name="contributed-resource-pending-detail"),
 #create
    url(r'^core-activities/capacity-development/guides-and-training-materials/contributed-resource-create/$',
        view=contribuitedresource_create, name="contribuited-resource-create"),
    #edit
        url(r'^core-activities/capacity-development/guides-and-training-materials/contributed-resource-list/edit/(?P<id>\d+)/$',
        view=contribuitedresource_edit, name="contribuited-resource-edit"),
        
   
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

#---------- USER MEMBERSHIP HISTORY ------------------------------#


  url(r'^work-area/user_membership/$',
        view=UserMembershipHistoryListView.as_view(),
        name='usermembershiphistory-list'),

    url(r'^work-area/user_membership/(?P<pk>\d+)/$',
        view=UserMembershipHistoryDetailView.as_view(),
        name="usermembershiphistory-detail"),
        

    url(r'^work-area/user_membership/create/$',
        view=usermembershiphistory_create,
        name='usermembershiphistory-create'),

    url(r'^work-area/user_membership/edit/(?P<id>\d+)/$',
        view=usermembershiphistory_edit,
        name='usermembershiphistory-edit'),
#---------------------MEDIA KIT


  url(r'^publications/$',
        view=MediaKitDocumentListView.as_view(),
        name='mediakit-list'),

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
