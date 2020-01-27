
from django.conf.urls import patterns, url

from mezzanine.conf import settings
from mezzanine.core.views import direct_to_template
from .views import CourseListView,CourseDetailView,ModuleListView,ModuleDetailView,LessonDetailView,QuizDetailView,question_answer,course_enroll,course_certificate,CertPDFView,eLearnAutoRegistrationListView,auto_register_elearn,auto_register_elearn_approve,auto_register_elearn_delete,requestaccess,course_certificateall

#-------------- PCE ---------------------------------#
urlpatterns = patterns("learn.views",  
    url(r"^$", direct_to_template, {"template": "learn/index.html"}, name="e-learning"),
 
   
    #COURSE:
    url(r'^courses/$', view=CourseListView.as_view(), name='course-list'),
    url(r'^courses/(?P<pk>\d+)/$',   view=CourseDetailView.as_view(), name='course-detail'),
    url(r'^courses/(?P<id>\d+)/modules/$',   view=ModuleListView.as_view(), name='module-list'),
    url(r'^courses/(?P<id>\d+)/modules/(?P<pk>\d+)/$',   view=ModuleDetailView.as_view(), name='module-detail'),
    url(r'^courses/(?P<id>\d+)/modules/(?P<moduleid>\d+)/lessons/(?P<pk>\d+)/$',   view=LessonDetailView.as_view(), name='lesson-detail'),
    url(r'^courses/(?P<id>\d+)/modules/(?P<moduleid>\d+)/quiz/(?P<pk>\d+)/$',   view=QuizDetailView.as_view(), name='quiz-detail'),
    url(r'^courses/(?P<courseid>\d+)/quiz/(?P<quizid>\d+)/question/(?P<qtype>\d+)/(?P<pk>\d+)/$', view=question_answer, name='question-answer'),
    url(r'^courses/(?P<courseid>\d+)/enroll/$',view=course_enroll,  name='course-enroll'),
    url(r'^courses/certificate/(?P<id>\d+)/$', view=course_certificate, name='certificate'),
    url(r'^courses/certificateall/(?P<id>\d+)/$', view=course_certificateall, name='certificate'),
    url(r'^courses/certificate/(?P<pk>\d+)/pdf/$', view=CertPDFView.as_view(), name='certificate-pdf'),
    
    #---------AUTO-REGISTER-USER ------------------------------#    
    url(r'^accounts/pendingapproval/$',eLearnAutoRegistrationListView.as_view(), name='index'),
    url(r'^accounts/autoregister/$',view=auto_register_elearn,name='auto-register'),
    url(r'^accounts/autoregister/approve/(?P<id>\d+)/$',view=auto_register_elearn_approve,name='auto-register-approve'),
    url(r'^accounts/autoregister/delete/(?P<id>\d+)/$',view=auto_register_elearn_delete,name='auto-register-delete'),
    url(r'^accounts/requestaccess/$',view=requestaccess,name='request-acccess'),
 
   
  
)
