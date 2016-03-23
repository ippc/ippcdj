
from django.conf.urls import patterns, url

from mezzanine.conf import settings
from mezzanine.core.views import direct_to_template
from .views import PceDashboardListView,PceVersionDetailView,PceSessionListView,\
    pceversion_create,pceversion_edit_step1,pceversion_edit_step2,pceversion_edit_step3,pceversion_edit_step4,\
    ModuleListView,\
    stakeholders_create,stakeholders_edit,StakeholdersListView,\
    problemanalysis_create,problemanalysis_edit,ProblemAnalysisListView,\
    swotanalysis_create,swotanalysis_edit,SwotAnalysisListView,\
    logicalframework_create,logicalframework_edit,LogicalFrameworkListView,\
    module1_create,module1_edit,module2_create,module2_edit, module3_create,module3_edit,module4_create,module4_edit,\
    module5_create,module5_edit,module6_create,module6_edit,module7_create,module7_edit,module8_create,module8_edit,\
    module9_create,module9_edit,module10_create,module10_edit,module11_create,module11_edit,\
    module12_create,module12_edit, module13_create,module13_edit,\
    pceversion_close,module_validate,module_unvalidate,module_sendtovalidator,\
    Module1ListView,Module2ListView,Module3ListView,Module4ListView,Module5ListView,Module6ListView,\
    Module7ListView,Module8ListView,Module9ListView,Module10ListView,Module11ListView,Module12ListView,Module13ListView,\
    generate_report,pceversion_completed,StakeholdersListPDFView,ProblemAnalysisListPDFView,SwotAnalysisListPDFView,LogicalFrameworkListPDFView,\
    Module1ListPDFView,Module2ListPDFView ,Module4ListPDFView,Module5ListPDFView,Module6ListPDFView,Module7ListPDFView,Module8ListPDFView,\
    Module9ListPDFView,Module10ListPDFView,Module11ListPDFView,Module12ListPDFView,Module13ListPDFView,Module3ListPDFView

#-------------- PCE ---------------------------------#
urlpatterns = patterns("pce.views",
    url(r"^$", direct_to_template, {"template": "pce/index.html"}, name="pce"),
 
    #TRAINING MATERIAL
    url(r'^training_material/$', direct_to_template, {"template": "pce/training_material_page.html"}, name="pce"),
   
    #DASHBOARD-list of sessions:
    url(r'^(?P<country>[\w-]+)/sessions/$', view=PceSessionListView.as_view(), name='pce-session-list'),
    url(r'^(?P<country>[\w-]+)/session/create_step1/$', view=pceversion_create, name='pceversion-create'),
    url(r'^(?P<country>[\w-]+)/session/create_step1/(?P<id>\d+)/$', view=pceversion_edit_step1, name='pceversion-edit-1'),
    url(r'^(?P<country>[\w-]+)/session/create_step2/(?P<id>\d+)/$', view=pceversion_edit_step2, name='pceversion-edit-2'),
    url(r'^(?P<country>[\w-]+)/session/create_step3/(?P<id>\d+)/$', view=pceversion_edit_step3, name='pceversion-edit-3'),
    url(r'^(?P<country>[\w-]+)/session/create_step4/(?P<id>\d+)/$', view=pceversion_edit_step4, name='pceversion-edit-4'),
    #DASHBOARD
    url(r'^(?P<country>[\w-]+)/session/dashboard/(?P<id>\d+)/$', view=PceDashboardListView.as_view(), name='pceversion-list'),
    #DASHBOARD-closesession
    url(r'^(?P<country>[\w-]+)/closesession/(?P<id>\d+)/$',view=pceversion_close,  name='pceversion_close'),
    #DASHBOARD-closesession
    url(r'^(?P<country>[\w-]+)/completesession/(?P<id>\d+)/$',view=pceversion_completed,  name='pceversion_completed'),
    #REPORT
    url(r'^(?P<country>[\w-]+)/report/(?P<sessionid>\d+)/$',view=generate_report,  name='generate_report'),

    #VALIDATEMODULE
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module(?P<module>\d+)/validate/(?P<id>\d+)/$',view=module_validate,  name='module_validate'),
    #UN-VALIDATEMODULE
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module(?P<module>\d+)/unvalidate/(?P<id>\d+)/$',view=module_unvalidate,  name='module_unvalidate'),
    #SENT TO VALIDATOR
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module(?P<module>\d+)/send/(?P<id>\d+)/$',view=module_sendtovalidator,  name='module_sendtovalidator'),
        
    #MODULE LIST:
    url(r'^(?P<country>[\w-]+)/session/(?P<id>\d+)/modules/$',   view=ModuleListView.as_view(), name='module-list'),
    #url(r'^(?P<country>[\w-]+)/pceversion/(?P<pk>\d+)/$', view=PceVersionDetailView.as_view(),name="pceversion-detail"),
    
    #MODULE 1:
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module1/edit/$', view=module1_create, name='module1-create'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module1/edit/(?P<id>\d+)/$', view=module1_edit, name='module1-edit'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module1/view/(?P<id>\d+)/$', view=Module1ListView.as_view(), name='module1-view'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module1/empty/$', view=Module1ListView.as_view(), name='module1-empty'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module1/pdf/(?P<id>\d+)/$', view=Module1ListPDFView.as_view(), name='module1-pdf'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module1/pdf_empty/$', view=Module1ListPDFView.as_view(), name='module1-pdf-empty'),
   
    #MODULE 2:
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module2/edit/$', view=module2_create, name='module2-create'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module2/edit/(?P<id>\d+)/$', view=module2_edit, name='module2-edit'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module2/view/(?P<id>\d+)/$', view=Module2ListView.as_view(), name='module2-view'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module2/empty/$', view=Module2ListView.as_view(), name='module2-view'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module2/pdf/(?P<id>\d+)/$', view=Module2ListPDFView.as_view(), name='module2-pdf'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module2/pdf_empty/$', view=Module2ListPDFView.as_view(), name='module2-pdf-empty'),
   
   #MODULE 3:
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module3/edit/$', view=module3_create, name='module3-create'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module3/edit/(?P<id>\d+)/$', view=module3_edit, name='module3-edit'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module3/view/(?P<id>\d+)/$', view=Module3ListView.as_view(), name='module3-view'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module3/empty/$', view=Module3ListView.as_view(), name='module3-empty'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module3/pdf/(?P<id>\d+)/$', view=Module3ListPDFView.as_view(), name='module3-pdf'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module3/pdf_empty/$', view=Module3ListPDFView.as_view(), name='module3-pdf-empty'),
 #MODULE 4:
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module4/edit/$', view=module4_create, name='module4-create'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module4/edit/(?P<id>\d+)/$', view=module4_edit, name='module4-edit'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module4/view/(?P<id>\d+)/$', view=Module4ListView.as_view(), name='module4-view'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module4/empty/$', view=Module4ListView.as_view(), name='module4-empty'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module4/pdf/(?P<id>\d+)/$', view=Module4ListPDFView.as_view(), name='module4-pdf'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module4/pdf_empty/$', view=Module4ListPDFView.as_view(), name='module4-pdf-empty'),
    #MODULE 5:
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module5/edit/$', view=module5_create, name='module5-create'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module5/edit/(?P<id>\d+)/$', view=module5_edit, name='module5-edit'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module5/view/(?P<id>\d+)/$', view=Module5ListView.as_view(), name='module5-view'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module5/empty/$', view=Module5ListView.as_view(), name='module5-empty'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module5/pdf/(?P<id>\d+)/$', view=Module5ListPDFView.as_view(), name='module5-pdf'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module5/pdf_empty/$', view=Module5ListPDFView.as_view(), name='module5-pdf-empty'),
 #MODULE 6:
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module6/edit/$', view=module6_create, name='module6-create'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module6/edit/(?P<id>\d+)/$', view=module6_edit, name='module6-edit'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module6/view/(?P<id>\d+)/$', view=Module6ListView.as_view(), name='module6-view'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module6/empty/$', view=Module6ListView.as_view(), name='module6-empty'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module6/pdf/(?P<id>\d+)/$', view=Module6ListPDFView.as_view(), name='module6-pdf'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module6/pdf_empty/$', view=Module6ListPDFView.as_view(), name='module6-pdf-empty'),
#MODULE 7:
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module7/edit/$', view=module7_create, name='module7-create'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module7/edit/(?P<id>\d+)/$', view=module7_edit, name='module7-edit'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module7/view/(?P<id>\d+)/$', view=Module7ListView.as_view(), name='module7-view'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module7/empty/$', view=Module7ListView.as_view(), name='module7-empty'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module7/pdf/(?P<id>\d+)/$', view=Module7ListPDFView.as_view(), name='module7-pdf'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module7/pdf_empty/$', view=Module7ListPDFView.as_view(), name='module7-pdf-empty'),
  #MODULE 8:
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module8/edit/$', view=module8_create, name='module8-create'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module8/edit/(?P<id>\d+)/$', view=module8_edit, name='module8-edit'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module8/view/(?P<id>\d+)/$', view=Module8ListView.as_view(), name='module8-view'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module8/empty/$', view=Module8ListView.as_view(), name='module8-empty'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module8/pdf/(?P<id>\d+)/$', view=Module8ListPDFView.as_view(), name='module8-pdf'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module8/pdf_empty/$', view=Module8ListPDFView.as_view(), name='module8-pdf-empty'),
    #MODULE 9:
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module9/edit/$', view=module9_create, name='module9-create'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module9/edit/(?P<id>\d+)/$', view=module9_edit, name='module9-edit'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module9/view/(?P<id>\d+)/$', view=Module9ListView.as_view(), name='module9-view'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module9/empty/$', view=Module9ListView.as_view(), name='module9-empty'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module9/pdf/(?P<id>\d+)/$', view=Module9ListPDFView.as_view(), name='module9-pdf'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module9/pdf_empty/$', view=Module9ListPDFView.as_view(), name='module9-pdf-empty'),
  #MODULE 10:
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module10/edit/$', view=module10_create, name='module10-create'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module10/edit/(?P<id>\d+)/$', view=module10_edit, name='module10-edit'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module10/view/(?P<id>\d+)/$', view=Module10ListView.as_view(), name='module10-view'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module10/empty/$', view=Module10ListView.as_view(), name='module10-empty'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module10/pdf/(?P<id>\d+)/$', view=Module10ListPDFView.as_view(), name='module10-pdf'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module10/pdf_empty/$', view=Module10ListPDFView.as_view(), name='module10-pdf-empty'),
 #MODULE 11:
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module11/edit/$', view=module11_create, name='module11-create'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module11/edit/(?P<id>\d+)/$', view=module11_edit, name='module11-edit'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module11/view/(?P<id>\d+)/$', view=Module11ListView.as_view(), name='module11-view'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module11/empty/$', view=Module11ListView.as_view(), name='module11-empty'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module11/pdf/(?P<id>\d+)/$', view=Module11ListPDFView.as_view(), name='module11-pdf'),
     url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module11/pdf_empty/$', view=Module11ListPDFView.as_view(), name='module11-pdf-empty'),
#MODULE 12:
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module12/edit/$', view=module12_create, name='module12-create'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module12/edit/(?P<id>\d+)/$', view=module12_edit, name='module12-edit'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module12/view/(?P<id>\d+)/$', view=Module12ListView.as_view(), name='module12-view'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module12/empty/$', view=Module12ListView.as_view(), name='module12-empty'),
     url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module12/pdf/(?P<id>\d+)/$', view=Module12ListPDFView.as_view(), name='module12-pdf'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module12/pdf_empty/$', view=Module12ListPDFView.as_view(), name='module12-pdf-empty'),
#MODULE 13:
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module13/edit/$', view=module13_create, name='module13-create'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module13/edit/(?P<id>\d+)/$', view=module13_edit, name='module13-edit'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module13/view/(?P<id>\d+)/$', view=Module13ListView.as_view(), name='module13-view'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module13/empty/$', view=Module13ListView.as_view(), name='module13-empty'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module13/pdf/(?P<id>\d+)/$', view=Module13ListPDFView.as_view(), name='module13-pdf'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/module13/pdf_empty/$', view=Module13ListPDFView.as_view(), name='module13-pdf-empty'),

    #Stakeholders:
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/(?P<module>\d+)/stakeholders/edit/$', view=stakeholders_create, name='stakeholders-edit'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/(?P<module>\d+)/stakeholders/edit/(?P<id>\d+)/$', view=stakeholders_edit, name='stakeholders-edit'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/(?P<module>\d+)/stakeholders/view/$', view=StakeholdersListView.as_view(), name='stakeholders-view'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/(?P<module>\d+)/stakeholders/view/(?P<id>\d+)/$', view=StakeholdersListView.as_view(), name='stakeholders-list'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/(?P<module>\d+)/stakeholders/pdf/(?P<id>\d+)/$', view=StakeholdersListPDFView.as_view(), name='stakeholders-pdf'),
   
    #ProblemAnalysis:
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/(?P<module>\d+)/problemanalysis/edit/$', view=problemanalysis_create, name='problemanalysis-edit'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/(?P<module>\d+)/problemanalysis/edit/(?P<id>\d+)/$', view=problemanalysis_edit, name='problemanalysis-edit'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/(?P<module>\d+)/problemanalysis/view/$', view=ProblemAnalysisListView.as_view(), name='problemanalysis-view'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/(?P<module>\d+)/problemanalysis/(?P<id>\d+)/$', view=ProblemAnalysisListView.as_view(), name='problemanalysis-list'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/(?P<module>\d+)/problemanalysis/pdf/(?P<id>\d+)/$', view=ProblemAnalysisListPDFView.as_view(), name='problemanalysis-pdf'),
   
    #SwotAnalysis:
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/(?P<module>\d+)/swotanalysis/edit/$', view=swotanalysis_create, name='swotanalysis-edit'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/(?P<module>\d+)/swotanalysis/view/$', view=SwotAnalysisListView.as_view(), name='swotanalysis-view'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/(?P<module>\d+)/swotanalysis/edit/(?P<id>\d+)/$', view=swotanalysis_edit, name='swotanalysis-edit'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/(?P<module>\d+)/swotanalysis/(?P<id>\d+)/$', view=SwotAnalysisListView.as_view(), name='swotanalysis-list'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/(?P<module>\d+)/swotanalysis/pdf/(?P<id>\d+)/$', view=SwotAnalysisListPDFView.as_view(), name='swotanalysis-pdf'),
    
   

    #LogicalFramework:
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/(?P<module>\d+)/logicalframework/edit/$', view=logicalframework_create, name='logicalframework-edit'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/(?P<module>\d+)/logicalframework/view/$', view=LogicalFrameworkListView.as_view(), name='logicalframework-view'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/(?P<module>\d+)/logicalframework/edit/(?P<id>\d+)/$', view=logicalframework_edit, name='logicalframework-edit'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/(?P<module>\d+)/logicalframework/(?P<id>\d+)/$', view=LogicalFrameworkListView.as_view(), name='logicalframework-list'),
    url(r'^(?P<country>[\w-]+)/(?P<sessionid>\d+)/(?P<module>\d+)/logicalframework/pdf/(?P<id>\d+)/$', view=LogicalFrameworkListPDFView.as_view(), name='logicalframework-pdf'),
    
   

)
