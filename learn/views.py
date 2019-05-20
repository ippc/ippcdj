
#import autocomplete_light
#autocomplete_light.autodiscover()
# -- coding: utf-8 --
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages import info, error
from django.utils import timezone
from django.core import mail
from django.conf import settings

from django.contrib.auth.models import User,Group
from symbol import except_clause
from ippc.models import  CountryPage,IppcUserProfile

from .models import Course, Module,Lesson,Category,Resource,Quiz,Question,QuestionField,QuestionResult,QuestionM,QuestionMultiField,QuestionMultiVal,eLearnAutoRegistration
from .forms import QuestionForm,eLearnAutoRegistrationForm
        
    

from django.views.generic import ListView, MonthArchiveView, YearArchiveView, DetailView, TemplateView, CreateView
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.template.defaultfilters import slugify, lower
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.forms.models import inlineformset_factory
from django.contrib.contenttypes.generic import generic_inlineformset_factory 
from django.forms.formsets import formset_factory
from compiler.pyassem import order_blocks
import time
from django.http import HttpResponse
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from mezzanine.generic import views as myview
from mezzanine.generic import models
from t_eppo.models import Names
from easy_pdf.views import PDFTemplateView
from django.utils.translation import ugettext
import random

import os
import shutil

import zipfile
import StringIO
from settings import PROJECT_ROOT, MEDIA_ROOT,DATABASES
from django.core.files.storage import default_storage

import getpass, imaplib, email
from xml.dom import minidom
import MySQLdb
from docx import Document
from docx.shared import Inches,Pt,Cm
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from django.utils.translation import ugettext, ugettext_lazy as _
from docx.oxml.ns import nsdecls, qn
from docx.oxml import parse_xml, OxmlElement
  
from docx.enum.section import WD_ORIENT
from docx.shared import RGBColor
def get_profile():
    return IppcUserProfile.objects.all()


class CourseListView(ListView):
    context_object_name = 'latest'
    model = Course
    date_field = 'publish_date'
    template_name = 'learn/course_list.html'
    queryset = Course.objects.all().order_by('title')
    allow_future = False
    allow_empty = True
    paginate_by = 500

     
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(CourseListView, self).get_context_data(**kwargs)
        categories = Category.objects.all().order_by('title')
        
        canseecourse=0
        user = self.request.user  
        is_in_group=user.groups.filter(name='eLearn').count()>0
        if  user.groups.filter(name='Admin') or (is_in_group):
            canseecourse=1
       
        allcategories=''
        enrolledcourse='<ul>'
        for cat in categories:
            allcategories+='<div><h4>'+cat.title+'</a></h4><div><ul>'
            courses =Course.objects.filter(status=2, category=cat).order_by('title')
            
            for course in courses:
                enrolledusers=course.enrolledusers
                if user in course.enrolledusers.all():
                    enrolledcourse+='<li>'+course.title+'</li>'
                    allcategories+='<li><h5><a href="/e-learning/courses/'+str(course.id)+'/">'+course.title+'</a>&#160; <span style="color:orange"><strong>Enrolled</strong></span> </h5></li>'
                else:
                    allcategories+='<li><h5>'+course.title+' &#160; <a class="btn btn-small btn-success" href="/e-learning/courses/'+str(course.id)+'/enroll/">Enroll</a></h5></li>'
            allcategories+='</ul></div></div>'
        enrolledcourse+='</ul>'        
          
   
        context['canseecourse']=canseecourse
        context['categories']=allcategories
        context['enrolledcourse']=enrolledcourse
        return context
    


class CourseDetailView(DetailView):
    """ Course detail page """
    model = Course
    context_object_name = 'course'
    template_name = 'learn/course_detail.html'
    queryset = Course.objects.filter(status=2)
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        course= get_object_or_404(Course, id=self.kwargs['pk'])
        canseecourse=0
        user = self.request.user  
        is_in_group=user.groups.filter(name='eLearn').count()>0
        enrolled=0
        enrolledusers=course.enrolledusers
        if user in course.enrolledusers.all():
             enrolled=1  
        if  user.groups.filter(name='Admin') or (is_in_group and enrolled):
            canseecourse=1
        
        context['canseecourse']=canseecourse
        
        return context   

class ModuleListView(ListView):
    context_object_name = 'latest'
    model = Module
    date_field = 'publish_date'
    template_name = 'learn/module_list.html'
    queryset = Module.objects.all().order_by('title')
    allow_future = False
    allow_empty = True
    paginate_by = 500

     
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(ModuleListView, self).get_context_data(**kwargs)
       
        course = get_object_or_404(Course, id=self.kwargs['id'])
        modules = Module.objects.filter(course=course)
     
        canseecourse=0
        enrolled=0
        user = self.request.user  
        is_in_group=user.groups.filter(name='eLearn').count()>0
        enrolledusers=course.enrolledusers
        if user in course.enrolledusers.all():
            enrolled=1
        
        if  user.groups.filter(name='Admin') or (is_in_group and enrolled):
            canseecourse=1
        context['canseecourse']=canseecourse
        context['course']=course
        context['modules']=modules
        context['has_cert']=course.has_certificate
       
       
        return context
    


class ModuleDetailView(DetailView):
    """ Course detail page """
    model = Module
    context_object_name = 'module'
    template_name = 'learn/module_detail.html'
    queryset = Module.objects.filter()
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(ModuleDetailView, self).get_context_data(**kwargs)
        course = get_object_or_404(Course, id=self.kwargs['id'])
        module = get_object_or_404(Module, id=self.kwargs['pk'])
        modules = Module.objects.filter(course=course)
        module_prev=''
        module_next=''
        print('xxxxxxxxxxxxxxxxxxxxx')
        if module.previousmodule != 0:
            module_p = get_object_or_404(Module, id=module.previousmodule)
            module_prev=module_p.title
        if module.nextmodule != 0:
            module_n = get_object_or_404(Module, id=module.nextmodule)
            module_next=module_n.title
        
        lessons = Lesson.objects.filter(module=module).order_by('id')
        quiz = Quiz.objects.filter(module=module).order_by('_order')
     
        canseecourse=0
        enrolled=0
        user = self.request.user  
        is_in_group=user.groups.filter(name='eLearn').count()>0
        enrolledusers=course.enrolledusers
        if user in course.enrolledusers.all():
            enrolled=1
        
        if  user.groups.filter(name='Admin') or (is_in_group and enrolled):
            canseecourse=1
        context['canseecourse']=canseecourse
        
        
        
        
        
        context['course']=course
        context['module']=module
        context['lessons']=lessons
        context['modules']=modules
        context['quiz']=quiz
        context['module_prev']=module_prev
        context['module_next']=module_next
       
        return context   


class LessonDetailView(DetailView):
    """ Course detail page """
    model = Lesson
    context_object_name = 'lesson'
    template_name = 'learn/lesson_detail.html'
    queryset = Lesson.objects.filter()
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        course = get_object_or_404(Course, id=self.kwargs['id'])
        modules = Module.objects.filter(course=course)
        module = get_object_or_404(Module, id=self.kwargs['moduleid'])
        lesson = get_object_or_404(Lesson, id=self.kwargs['pk'])
        print('ssssssssssssssssssss')
        
        lessons = Lesson.objects.filter(module=module).order_by('_order')
        resource=None
        try:
            resource = get_object_or_404(Resource, module=module,course=course)
        except:
            resource=None
        
        quiz = Quiz.objects.filter(module=module).order_by('_order')
 
        context['quiz']=quiz
        
        canseecourse=0
        enrolled=0
        user = self.request.user  
        is_in_group=user.groups.filter(name='eLearn').count()>0
        enrolledusers=course.enrolledusers
        if user in course.enrolledusers.all():
            enrolled=1
        
        if  user.groups.filter(name='Admin') or (is_in_group and enrolled):
            canseecourse=1
        context['canseecourse']=canseecourse
        context['course']=course
        context['module']=module
        context['lesson']=lesson
        context['modules']=modules
        context['lessons']=lessons
        context['resource']=resource
        
     
        return context      
    
class QuizDetailView(DetailView):
    """ Course detail page """
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'learn/quiz_detail.html'
    queryset = Quiz.objects.filter()
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(QuizDetailView, self).get_context_data(**kwargs)
        
        course = get_object_or_404(Course, id=self.kwargs['id'])
        user = self.request.user
        
        canseecourse=0
        enrolled=0
        user = self.request.user  
        is_in_group=user.groups.filter(name='eLearn').count()>0
        enrolledusers=course.enrolledusers
        if user in course.enrolledusers.all():
            enrolled=1
        if  user.groups.filter(name='Admin') or (is_in_group and enrolled):
            canseecourse=1
            
        modules = Module.objects.filter(course=course)
        module = get_object_or_404(Module, id=self.kwargs['moduleid'])
        quiz = get_object_or_404(Quiz, id=self.kwargs['pk'])
        questions = Question.objects.filter(quiz=quiz).order_by('_order')
        countquestions=questions.count()
        questionMs = QuestionM.objects.filter(quiz=quiz).order_by('_order')
        countquestionMs=questionMs.count()
        finalcountquestion=countquestions+countquestionMs
        
        quizattemptresult=0
        
        print('-------------finalcountquestion------------------')
        print(finalcountquestion)
        print('-------------------------------')
        sumresult=0
        
        for q in questions:
            results  = QuestionResult.objects.filter(question_id=q.id, userquestion_id=user.id)
            if results.count()>0:
                res=results[0].result
                sumresult=sumresult+int(res)
        for q in questionMs:
            results  = QuestionResult.objects.filter(question_id=q.id, userquestion_id=user.id)
            if results.count()>0:
                res=results[0].result
                print(res)
                sumresult=sumresult+int(res)
        print(sumresult)    
        print('-------------------------------')
        quizattemptresult=sumresult/finalcountquestion 
        print(quizattemptresult)    
        print('-------------------------------')
        alreadyattempt='NO'
        if results.count()>0:
            alreadyattempt='YES'    
        
        context['canseecourse']=canseecourse
        context['course']=course
        context['module']=module
        context['quiz']=quiz
        context['modules']=modules
        context['questions']=questions
        context['questionMs']=questionMs
        context['alreadyattempt']=alreadyattempt
        context['quizattemptresult']=quizattemptresult
        
        
     
        return context      
      
@login_required
@permission_required('learn.add_question', login_url="/accounts/login/")
def question_answer(request, quizid=None, courseid=None,pk=None,qtype=None, ):
    """ Create question  """
    user = request.user
    canseecourse=0
    enrolled=0
    questions=[]
    questionMs=[]
    countchoiceM=0
    countchoice=0
    course = get_object_or_404(Course,  id=courseid)
    quiz = get_object_or_404(Quiz,  id=quizid)
    is_in_group=user.groups.filter(name='eLearn').count()>0
    enrolledusers=course.enrolledusers
    if user in course.enrolledusers.all():
        enrolled=1
    if  user.groups.filter(name='Admin') or (is_in_group and enrolled):
        canseecourse=1
    results_id=''
    results  = QuestionResult.objects.filter(question_id=pk, userquestion_id=user.id)
    if results.count()>0:
        results_id=str(results[0].id)
    
    question=None
    questionM=None
    fieldsMultiVal=''
    arrayfields=[]
           
    if qtype == '1':
        try:
           question = get_object_or_404(Question,  id=pk)
           questions  =Question.objects.filter(quiz_id=quizid)
           fields=QuestionField.objects.filter(question_id=question.id)
           countchoice=fields.count()
        except:
           question=None
    if qtype == '2':
        
        try:
            questionM = get_object_or_404(QuestionM,  id=pk)
            questionMs  =QuestionM.objects.filter(quiz_id=quizid)
            fieldsM=QuestionMultiField.objects.filter(question_id=questionM.id)
            countchoiceM=fieldsM.count()

            
            for ff in fieldsM:
                arrayfields1=[]
                options=''
                fieldsVal=QuestionMultiVal.objects.filter(question_id=ff.id)
                i=0
                value=0
                values=[]
                for vals in fieldsVal:
                     vall=str(i)
                     #options+='<option value="'+vall+'">'+vals.value+'</option>'
                     if vals.answer==True:
                         value=i
                     i+=1
                     values.append(vals.value)
                arrayfields1.append(ff.text)     
                arrayfields1.append(ff.id)
                arrayfields1.append(value)
                
                arrayfields1.append(values)
                arrayfields.append(arrayfields1)
#        for ff in fieldsM:
#                options=''
#                fieldsVal=QuestionMultiVal.objects.filter(question_id=ff.id)
#                i=0
#                value=0
#                for vals in fieldsVal:
#                     vall=str(i)
#                     options+='<option value="'+vall+'">'+vals.value+'</option>'
#                     if vals.answer==True:
#                         value=i
#                     i+=1
#                fieldsMultiVal+='<tr><td>'+str(ff)+'</td><td> <select name="sel_'+str(ff.id)+'"value="'+str(value)+'">  <option value="" selected disabled hidden>Choose here</option>'+options+'</select></td></tr>'

        except:
            questionM=None
  
  
    if request.method == "POST":
        form = QuestionForm()
        
        points=0
        
        if question!=None:
            nextq=question.nextq
            if question.q_type == 1:
                points=0
                result=0
                for f in fields:
                    val=''
                    for pp in request.POST:
                        if pp == 'q_choice'+str(f.id):
                            val=request.POST['q_choice'+str(f.id)]
                    if f.answer==1 and val== 'on':
                       points=points+1 
                    if f.answer==0 and val== '':
                       points=points+1    
                result= (points *  100)/countchoice
            elif question.q_type == 2:
                points=0
                result=0
                val=''
                for pp in request.POST:
                   if pp == 'q_choice'+str(question.id):
                       val=request.POST['q_choice'+str(question.id)]
                if  val == 'True':
                   result=  100
        if questionM!=None:
            nextq=questionM.nextq
            if questionM.q_type == 3:
                points=0
                result=0
                val=''
                for ff in fieldsM:
                    fieldsVal=QuestionMultiVal.objects.filter(question_id=ff.id)
                    i=0
                    value=0
                    for vals in fieldsVal:
                        if vals.answer==True:
                            value=i
                        i+=1
                    for pp in request.POST:
                        if pp == 'sel_'+str(ff.id):
                            val=request.POST['sel_'+str(ff.id)]
                            print('val of dropdpown='+str(val))
                            if val == str(value):
                                print(' YESSSSS')
                                points+=1
                result= (points *  100)/countchoiceM                
                  
            
      
        print('------- result -------')    
        print(result)    
        print('--------------')    
        sql = ""
        q_id=0
        qnextq_type=0
        
        if question!=None:
            q_id=question.id
            qnextq_type=question.nextq_type
        if questionM!=None:
            q_id=questionM.id
            qnextq_type=questionM.nextq_type
        if results_id == '':
             sql = "INSERT INTO learn_questionresult(question_id,userquestion_id,quiz_id,result,q_latest_date) VALUES ("+str(q_id)+", '"+str(user.id)+"', "+str(quiz.id)+", '"+str(result)+"','"+str(datetime.today())+"');"
        else:
            sql = "UPDATE learn_questionresult set result= '"+str(result)+"' where  question_id="+str(q_id)+", q_latest_date='"+str(datetime.today())+"';"
        
        print(sql)    
        
        db = MySQLdb.connect(DATABASES["default"]["HOST"],DATABASES["default"]["USER"],DATABASES["default"]["PASSWORD"],DATABASES["default"]["NAME"])
        cursor = db.cursor()
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    
        if  nextq == 0 :
            return redirect("quiz-detail",id=course.id,moduleid=quiz.module.id,pk=quiz.id)
        else:    
            return redirect("question-answer",courseid=course.id,quizid=quiz.id,pk=nextq,qtype=qnextq_type)
     
    else:
        form = QuestionForm()
       
    
    return render_to_response('learn/questionform.html', {'form': form,'quiz':quiz,'course':course,'question':question,'questionM':questionM,'questions':questions,'questionMs':questionMs,'arrayfields':arrayfields,'fieldsMultiVal':fieldsMultiVal,'canseecourse':canseecourse},
            context_instance=RequestContext(request))
  
@login_required
@permission_required('learn.add_course', login_url="/accounts/login/")
def course_enroll(request, courseid=None ):
    """ VALIDATE Module """
    user = request.user
    course = get_object_or_404(Course,  id=courseid)
    enrolledusers=course.enrolledusers
    if user in course.enrolledusers.all():
        print("already enrolled")
    else:
        sql = "INSERT INTO learn_course_enrolledusers (course_id,user_id) VALUES ("+str(course.id)+", '"+str(user.id)+"');"
        db = MySQLdb.connect(DATABASES["default"]["HOST"],DATABASES["default"]["USER"],DATABASES["default"]["PASSWORD"],DATABASES["default"]["NAME"])
        cursor = db.cursor()
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
   
        
    info(request, _("Successfully Enrolled to course: "+str(course.title)+"."))
    return redirect("course-list", )

       
@login_required
@permission_required('learn.add_course', login_url="/accounts/login/")
def course_certificate(request, id=None):
    """ Create certificate  """
    course = get_object_or_404(Course,  id=id)
    
    user = request.user
    canseecourse=0
    enrolled=0
    quizzes_array=[]
    certgrade=0
    cert_ok=0
       
    is_in_group=user.groups.filter(name='eLearn').count()>0
    enrolledusers=course.enrolledusers
    if user in course.enrolledusers.all():
        enrolled=1
    if  user.groups.filter(name='Admin') or (is_in_group and enrolled):
        canseecourse=1
    
    if canseecourse==1 and course.has_certificate ==1:
        
        modules = Module.objects.filter(course=course)

        q_grade=0
        quizcount=0
        done_count=0
        q_ok_count=0
        for mod in modules:
            quiz=None
            try:
                quiz = get_object_or_404(Quiz,  module=mod)
            except:
                quiz=None
                
            if quiz!=None:
                quizcount+=1
                questions  =Question.objects.filter(quiz_id=quiz.id)
                countquestions=questions.count()
                questionMs  =QuestionM.objects.filter(quiz_id=quiz.id)
                countquestionMs=questionMs.count()
                final_countquestion=countquestionMs+countquestions
                done=0
                done_count=0
                sumresult=0
                for q in questions:
                    
                    results  = QuestionResult.objects.filter(question_id=q.id,quiz_id=quiz.id, userquestion_id=user.id)
                    print(results.count())
                    if results.count()>0:
                       done= 1
                       done_count+=1
                       sumresult=sumresult+int(results[0].result)
                    else:
                       done= 0
                for q in questionMs:
                    results  = QuestionResult.objects.filter(question_id=q.id,quiz_id=quiz.id, userquestion_id=user.id)
                    if results.count()>0:
                       done= 1
                       done_count+=1
                       sumresult=sumresult+int(results[0].result)
                    else:
                       done= 0       
                quiz_result=sumresult/final_countquestion
                q_ok=0
                if quiz_result >= int(quiz.quizgrade):
                    q_ok=1
                    q_ok_count+=1
                    
                quizz_array=[]
                quizz_array.append(quiz.title)
                quizz_array.append(done)
                quizz_array.append(q_ok)
                quizz_array.append(quiz_result)
                
                
                quizzes_array.append(quizz_array)
                q_grade=q_grade+quiz_result
                
           
        certgrade=  q_grade/ quizcount
        cert_ok=0
        if certgrade >= int(course.certificategrade) and done_count==quizcount and q_ok_count==quizcount:
            cert_ok=1
      
       
        return render_to_response('learn/certificate.html', {'course':course,'quizzes_array':quizzes_array,'certgrade':certgrade,'canseecourse':canseecourse,'cert_ok':cert_ok},
            context_instance=RequestContext(request))
  
    else:   
        return render_to_response('learn/certificate.html', {'course':course,'quizzes_array':quizzes_array,'certgrade':certgrade,'canseecourse':canseecourse,'cert_ok':cert_ok},
            context_instance=RequestContext(request))
            

class CertPDFView(PDFTemplateView):
    context_object_name = 'latest'
    model = Course
    template_name = 'learn/certificate_pdf.html'
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(CertPDFView, self).get_context_data(**kwargs)
        courseid = self.kwargs['pk']
        user = self.request.user
        canseecourse=0
        enrolled=0
        quizzes_array=[]
        certgrade=0
        cert_ok=0
        course = get_object_or_404(Course,  id=courseid)
        username=''
        
        is_in_group=user.groups.filter(name='eLearn').count()>0
        enrolledusers=course.enrolledusers
        if user in course.enrolledusers.all():
            enrolled=1
        if  user.groups.filter(name='Admin') or (is_in_group and enrolled):
            canseecourse=1

        if canseecourse==1 and course.has_certificate ==1:

            modules = Module.objects.filter(course=course)

            q_grade=0
            quizcount=0
            done_count=0
            q_ok_count=0
            for mod in modules:
                quiz=None
                try:
                    quiz = get_object_or_404(Quiz,  module=mod)
                except:
                    quiz=None

                if quiz!=None:
                    quizcount+=1
                    questions  =Question.objects.filter(quiz_id=quiz.id)
                    countquestions=questions.count()
                    questionMs  =QuestionM.objects.filter(quiz_id=quiz.id)
                    countquestionMs=questionMs.count()
                    final_countquestion=countquestionMs+countquestions
                
                    done=0
                    done_count=0
                    sumresult=0
                    for q in questions:
                        results  = QuestionResult.objects.filter(question_id=q.id, quiz_id=quiz.id,userquestion_id=user.id)
                        if results.count()>0:
                           done= 1
                           done_count+=1
                           res=results[0].result
                           sumresult=sumresult+int(res)
                        else:
                           done= 0
                    quiz_result=sumresult/final_countquestion
                    q_ok=0
                    if quiz_result>=int(quiz.quizgrade):
                        q_ok=1
                        q_ok_count+=1
                    quizz_array=[]
                    quizz_array.append(quiz.title)
                    quizz_array.append(done)
                    quizz_array.append(q_ok)
                    quizz_array.append(quiz_result)


                    quizzes_array.append(quizz_array)
                    q_grade=q_grade+quiz_result


            certgrade=  q_grade/ quizcount
            cert_ok=0
        if certgrade>=int(course.certificategrade) and done_count==quizcount and q_ok_count==quizcount:#and each Quiz has 60
            cert_ok=1
            userippc = get_object_or_404(IppcUserProfile, user_id=user.id)
            username=userippc.first_name+' '+userippc.last_name
      
        
        context['cert_ok'] = cert_ok
        context['coursetitle'] = course.title
        context['certgrade'] = certgrade
        context['datec'] = timezone.now().strftime('%d %B %Y')
        context['username'] = username
        
        
      
        
        return context
class eLearnAutoRegistrationListView(ListView):
    """    UserAutoRegistration List view """
    context_object_name = 'latest'
    model = eLearnAutoRegistration
    date_field = 'date'
    template_name = 'learn/elearn_accounts_list.html'
    queryset = eLearnAutoRegistration.objects.all().order_by('-publish_date')

from django.http import HttpResponseRedirect
#@login_required
def auto_register_elearn(request):
    """ auto_register """
    
    form =eLearnAutoRegistrationForm(request.POST)
    if request.method == "POST" :
         if form.is_valid() and request.POST['captcha'] ==  request.POST['result_element']:
            new_user = form.save(commit=False)
            form.save()
            info(request, _("Successfully registered to IPPC e-learning, the IPPC Team will revise your registration."))
            subject='A new user has self-registered for IPPC e-learning access'  
            msg='<p>A new user has self-registered for IPPC  e-learning access.<br><br>Please use the link below to view the list of users pending approval:<br><br><a href="https://www.ippc.int/e-learning/accounts/pendingapproval/">https://www.ippc.int/e-learning/accounts/pendingapproval/</a>.'
            message = mail.EmailMessage(subject,msg,'ippc@fao.org', ['ippc-it@fao.org'], ['paola.sentinelli@fao.org'])
            message.content_subtype = "html"
            #print('test-sending')
            sent =message.send()
            
            return HttpResponseRedirect("/e-learning/")
         else:
            error_captcha=''
            if not(request.POST['captcha'] == request.POST['result_element'] ) :
                error_captcha='error'
                  
            return render_to_response('learn/elearn_register_create.html', {'form': form,'x_element': request.POST['x_element'],'y_element': request.POST['y_element'],'result_element': request.POST['result_element'] ,'error_captcha':error_captcha},
            context_instance=RequestContext(request))
    else:
         x_element=random.randint(1,10)   
         y_element=random.randint(1,10)
         result_element=x_element+y_element
     
         form = eLearnAutoRegistrationForm()
# 
    return render_to_response('learn/elearn_register_create.html', {'form': form ,'x_element':x_element,'y_element':y_element,'result_element':result_element},
        context_instance=RequestContext(request))
     
    
@login_required
@permission_required('ippc.delete_group', login_url="/accounts/login/")
def auto_register_elearn_approve(request, id=None):
    """   auto_registerelearn_approve User approve  """
    
    if id:
       #print('APPROVED')
        newuser = get_object_or_404(eLearnAutoRegistration,  pk=id)
        user_obj=User.objects.filter(email=newuser.email)
        if user_obj.count()>0:
            newuser.status=3
            newuser.save()
            error(request, _("An user with the same email address is alredy registered in the system."))
            return HttpResponseRedirect("/e-learning/accounts/pendingapproval/")
        else:
            #create new user
            user1=User()
            user1.username=slugify(newuser.firstname+"-"+newuser.lastname).lower()
            user1.first_name=newuser.firstname
            user1.last_name=newuser.lastname
            user1.email=newuser.email
            user1.save()
            #set groups
            g1=Group.objects.get(name="elearn")
            user1.groups.add(g1)
            
            #set profile
            userp = get_object_or_404(IppcUserProfile, user_id=user1.id)
            userp.first_name=newuser.firstname
            userp.last_name=newuser.lastname
            #userp.country=newuser.country
            userp.address1=newuser.organisation
            userp.save()
            
            #sendmessage to new user
            user_email = []
            user_email.append(newuser.email)
            subject='Activate your account created for you at https://www.ippc.int/e-learning/'  
            msg='<p>An IPPC account has been created for you to access the e-learning courses.<br><br>Please use the link below to set your password.<br><br><a href="https://www.ippc.int/en/account/password/reset/?next=/en/account/update/">https://www.ippc.int/en/account/password/reset/?next=/en/account/update/</a><br><br>Insert your email address, click on "Password Reset" button and follow instructions to create your password.<br><br>After setting your password, you will be able to log in at https://www.ippc.int/e-learning .<br><br><br><br>Information Exchange (IPPC) team<br><br><br>he IPPC is an international treaty to secure action to prevent the spread and introduction of pests of plants and plant products, and to promote appropriate measures for their control. It is governed by the Commission on Phytosanitary Measures (CPM) which adopts International Standards for Phytosanitary Measures (ISPMs). The CPM established the IPP as the forum for national reporting and exchange of more general information among the phytosanitary community. The IPPC Secretariat coordinates the activities of the Convention and is hosted by FAO.'
                
            message = mail.EmailMessage(subject,msg,'ippc@fao.org', user_email, ['paola.sentinelli@fao.org'])
            message.content_subtype = "html"
            #print('test-sending')
            sent =message.send()
            #delete temporary user
            newuser.delete()
           
            info(request, _("Successfully approved user."))
            return HttpResponseRedirect("/e-learning/accounts/pendingapproval/")
       

@login_required
@permission_required('ippc.delete_group', login_url="/accounts/login/")
def auto_register_elearn_delete(request, id=None):
    """ auto registered User delete   """
    if id:
        newuser = get_object_or_404(eLearnAutoRegistration,  pk=id)
        newuser.delete()
     
        info(request, _("Successfully deleted user."))
        return HttpResponseRedirect("/e-learning/accounts/pendingapproval/")         
    
@login_required
def requestaccess(request ):
    """ send email """
    user = request.user
    requestor_email = []
         
    user_obj=User.objects.get(id=user.id)
    requestor_email.append(user_obj.email)

    subject='IPPC request access to e-learning courses'  
    msg='Dear IPPC,<br><br>this message is to request access to the e-learning courses for the user: '+user.first_name+' '+user.last_name+' '+requestor_email
    notifificationmessage = mail.EmailMessage(subject,msg,'ippc@fao.org',  ['ippc-it@fao.org'], ['ippc-it@fao.org'])
    notifificationmessage.content_subtype = "html"
    try:
        sent =notifificationmessage.send()
        info(request, _("Successfully SENT request."))
    except:
       print('ERROR sending')

                
    return HttpResponseRedirect("/e-learning/")   