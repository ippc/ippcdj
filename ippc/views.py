#import autocomplete_light
#autocomplete_light.autodiscover()

from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages import info, error
from django.utils import timezone
from django.core import mail
from django.conf import settings

from django.contrib.auth.models import User,Group
from .models import ContactType,PublicationLibrary,Publication,EppoCode,EmailUtilityMessage, EmailUtilityMessageFile, Poll_Choice, Poll,PollVotes, IppcUserProfile,\
CountryPage,PartnersPage, PestStatus, PestReport, IS_PUBLIC, IS_HIDDEN, Publication,\
DraftProtocol,DraftProtocolComments,NotificationMessageRelate,\
ReportingObligation, BASIC_REP_TYPE_CHOICES, EventReporting, EVT_REP_TYPE_CHOICES,Website,CnPublication,PartnersPublication,PartnersNews, PartnersWebsite,CountryNews, \
PestFreeArea,ImplementationISPM,REGIONS, IssueKeywordsRelate,CommodityKeywordsRelate,EventreportingFile,ReportingObligation_File
from mezzanine.core.models import Displayable, CONTENT_STATUS_DRAFT, CONTENT_STATUS_PUBLISHED
from .forms import PestReportForm,PublicationUrlFormSet,PublicationForm, PublicationFileFormSet, ReportingObligationForm, EventReportingForm, PestFreeAreaForm,\
ImplementationISPMForm,IssueKeywordsRelateForm,CommodityKeywordsRelateForm,EventreportingFileFormSet,ReportingoblicationFileFormSet,\
ImplementationISPMFileFormSet,PestFreeAreaFileFormSet, PestReportFileFormSet,WebsiteUrlFormSet,WebsiteForm, \
EventreportingUrlFormSet, ReportingObligationUrlFormSet ,PestFreeAreaUrlFormSet,ImplementationISPMUrlFormSet,PestReportUrlFormSet,\
CnPublicationUrlFormSet,CnPublicationForm, CnPublicationFileFormSet,\
PartnersPublicationUrlFormSet,PartnersPublicationForm, PartnersPublicationFileFormSet,\
PollForm,Poll_ChoiceFormSet,\
PartnersNewsUrlFormSet,PartnersNewsForm, PartnersNewsFileFormSet,PartnersWebsiteUrlFormSet,PartnersWebsiteForm,\
EmailUtilityMessageForm,EmailUtilityMessageFileFormSet,\
CountryNewsUrlFormSet,CountryNewsForm, CountryNewsFileFormSet,NotificationMessageRelateForm,\
DraftProtocolForm,  DraftProtocolFileFormSet,DraftProtocolCommentsForm,IppcUserProfileForm# , UserForm

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
def get_profile():
    return IppcUserProfile.objects.all()

# def pest_report_country():
#     return PestReport.objects.all()
def commenta(request, template="generic/comments.html"):
    """
    Handle a ``ThreadedCommentForm`` submission and redirect back to its
    related object.
    """
    response = myview.initial_validation(request, "comment")
    if isinstance(response, HttpResponse):
        return response
    obj, post_data = response
    print(obj.categories)
    emailto_all=[]
    #notification to Secretariat of comments
    for g in obj.groups.all():
       group=Group.objects.get(id=g.id)
       emailto_all.append(str('paola.sentinelli@fao.org'))

    subject='IPPC new comment on: '+str(obj)  
    #print(request.POST['name'])
    text=request.POST['name']+' has commented on: '+str(obj) +'<br><hr><br>'+request.POST['comment']
    
    
    #TO FIX with real message
    #notifificationmessage = mail.EmailMessage(subject,text,'paola.sentinelli@fao.org', emailto_all, ['paola.sentinelli@fao.org'])
    notifificationmessage = mail.EmailMessage(subject,text,'ippc@fao.org', emailto_all, ['paola.sentinelli@fao.org'])
    notifificationmessage.content_subtype = "html"
    sent =notifificationmessage.send()

    
    form = myview.ThreadedCommentForm(request, obj, post_data)
    if form.is_valid():
        url = obj.get_absolute_url()
        if myview.is_spam(request, form, url):
            return redirect(url)
        comment = form.save(request)
        response = redirect(myview.add_cache_bypass(comment.get_absolute_url()))
        # Store commenter's details in a cookie for 90 days.
        for field in myview.ThreadedCommentForm.cookie_fields:
            cookie_name = myview.ThreadedCommentForm.cookie_prefix + field
            cookie_value = post_data.get(field, "")
            myview.set_cookie(response, cookie_name, cookie_value)
        return response
    elif request.is_ajax() and form.errors:
        return HttpResponse(dumps({"errors": form.errors}))
    # Show errors with stand-alone comment form.
    context = {"obj": obj, "posted_comment_form": form}
    response = render(request, template, context)
    return response

class CountryView(TemplateView):
    """ 
    Individual country homepage 
    """
    template_name = 'countries/country_page.html'
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['event_types'] =EVT_REP_TYPE_CHOICES
        context['basic_types'] =BASIC_REP_TYPE_CHOICES 
        context.update({
            'country': self.kwargs['country']
            # 'editors': self.kwargs['editors']
            # 'profile_user': self.kwargs['profile_user']
        })
        return context


class PublicationLibraryView(ListView):
    """ 

    """
    template_name = 'pages/publicationlibrary.html'
    queryset = DraftProtocol.objects.all()
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(PublicationLibraryView, self).get_context_data(**kwargs)
        queryset = DraftProtocol.objects.all()
        context['latest1']=queryset
       
        users_sec=[]
        users_sc=[] 
        users_bureau=[]
        users_tpfq=[]
        users_tpdp=[]
        users_tpff=[]
        users_tpg=[]
        users_tppt=[]
        for g in Group.objects.filter():
            if g.name == 'IPPC Secretariat': 
                users = g.user_set.all()
                for u in users:
                   users_u=[]
                   user_obj=User.objects.get(username=u)
                   userippc = get_object_or_404(IppcUserProfile, user_id=user_obj.id)
                   users_u.append((unicode(userippc.last_name)))
                   users_u.append((unicode(userippc.first_name)))
                   users_u.append((userippc.profile_photo))
                   users_u.append((userippc.title))
                   users_u.append((user_obj.username))
                   users_sec.append(users_u)
            if g.name == 'Standards committee':
                users = g.user_set.all()
                for u in users:
                   users_u=[]
                   user_obj=User.objects.get(username=u)
                   userippc = get_object_or_404(IppcUserProfile, user_id=user_obj.id)
                   users_u.append((unicode(userippc.last_name)))
                   users_u.append((unicode(userippc.first_name)))
                   users_u.append((userippc.profile_photo))
                   users_u.append((userippc.title))
                   users_u.append((user_obj.username))
                   users_sc.append(users_u)
          
            if g.name == 'Bureau': 
                users = g.user_set.all()
                for u in users:
                   users_u=[]
                   user_obj=User.objects.get(username=u)
                   userippc = get_object_or_404(IppcUserProfile, user_id=user_obj.id)
                   users_u.append((unicode(userippc.last_name)))
                   users_u.append((unicode(userippc.first_name)))
                   users_u.append((userippc.profile_photo))
                   users_u.append((userippc.title))
                   users_u.append((user_obj.username))
                   users_bureau.append(users_u)
            if g.name == 'TPDP': 
                users = g.user_set.all()
                for u in users:
                   users_u=[]
                   user_obj=User.objects.get(username=u)
                   userippc = get_object_or_404(IppcUserProfile, user_id=user_obj.id)
                   users_u.append((unicode(userippc.last_name)))
                   users_u.append((unicode(userippc.first_name)))
                   users_u.append((userippc.profile_photo))
                   users_u.append((userippc.title))
                   users_u.append((user_obj.username))
                   users_tpdp.append(users_u)
            if g.name == 'TPFQ': 
                users = g.user_set.all()
                for u in users:
                   users_u=[]
                   user_obj=User.objects.get(username=u)
                   userippc = get_object_or_404(IppcUserProfile, user_id=user_obj.id)
                   users_u.append((unicode(userippc.last_name)))
                   users_u.append((unicode(userippc.first_name)))
                   users_u.append((userippc.profile_photo))
                   users_u.append((userippc.title))
                   users_u.append((user_obj.username))
                   users_tpfq.append(users_u)
            if g.name == 'TPFF': 
                users = g.user_set.all()
                for u in users:
                   users_u=[]
                   user_obj=User.objects.get(username=u)
                   userippc = get_object_or_404(IppcUserProfile, user_id=user_obj.id)
                   users_u.append((unicode(userippc.last_name)))
                   users_u.append((unicode(userippc.first_name)))
                   users_u.append((userippc.profile_photo))
                   users_u.append((userippc.title))
                   users_u.append((user_obj.username))
                   users_tpff.append(users_u)
            if g.name == 'TPG': 
                users = g.user_set.all()
                for u in users:
                   users_u=[]
                   user_obj=User.objects.get(username=u)
                   userippc = get_object_or_404(IppcUserProfile, user_id=user_obj.id)
                   users_u.append((unicode(userippc.last_name)))
                   users_u.append((unicode(userippc.first_name)))
                   users_u.append((userippc.profile_photo))
                   users_u.append((userippc.title))
                   users_u.append((user_obj.username))
                   users_tpg.append(users_u)
            if g.name == 'TPPT': 
                users = g.user_set.all()
                for u in users:
                   users_u=[]
                   user_obj=User.objects.get(username=u)
                   userippc = get_object_or_404(IppcUserProfile, user_id=user_obj.id)
                   users_u.append((unicode(userippc.last_name)))
                   users_u.append((unicode(userippc.first_name)))
                   users_u.append((userippc.profile_photo))
                   users_u.append((userippc.title))
                   users_u.append((user_obj.username))
                   #users_u.append((user_obj.contact_type))
                   users_tppt.append(users_u)
            
        
        context['secretariat']=users_sec
        context['users_sc']=users_sc
        context['users_bureau']=users_bureau
        context['users_tpdp']=users_tpdp
        context['users_tpff']=users_tpff
        context['users_tppt']=users_tppt
        context['users_tpg']=users_tpg
        context['users_tpfq']=users_tpfq
        return context
    def get_queryset(self):
        queryset = DraftProtocol.objects.all()
        return  DraftProtocol.objects.all()


class CountryRelatedView(TemplateView):
    """ 
    Individual country related info 
    """
    template_name = 'countries/country_related_info.html'
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(TemplateView, self).get_context_data(**kwargs)
        print(self.kwargs['country'])
        countryo= CountryPage.objects.filter(country_slug=self.kwargs['country'])
        context['iso3'] =countryo[0].iso3 
        context['cn_map'] =countryo[0].cn_map 
        context.update({
            'country': self.kwargs['country']
        })
        return context



class PestReportListView(ListView):
    """
    Pest reports
        http://stackoverflow.com/questions/8547880/listing-object-with-specific-tag-using-django-taggit
        http://stackoverflow.com/a/7382708/412329
    """
    context_object_name = 'latest'
    model = PestReport
    date_field = 'publish_date'
    template_name = 'countries/pest_report_list.html'
    queryset = PestReport.objects.all().order_by('-publish_date', 'title')
    allow_future = False
    allow_empty = True
    paginate_by = 30

    def get_queryset(self):
        """ only return pest reports from the specific country """
        # self.country = get_object_or_404(CountryPage, country=self.kwargs['country'])
        self.country = self.kwargs['country']
        # CountryPage country_slug == country URL parameter keyword argument
        return PestReport.objects.filter(country__country_slug=self.country, status=CONTENT_STATUS_PUBLISHED)
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(PestReportListView, self).get_context_data(**kwargs)
        context['country'] = self.kwargs['country']
        # context.update({
        #     'country': self.kwargs['country']
        # })
        return context

# @login_required
# @permission_required('ippc.add_pestreport', login_url="/accounts/login/")

class PestReportHiddenListView(ListView):
    """
    Hidden Pest reports so editors can still edit them
    """
    context_object_name = 'latest'
    model = PestReport
    date_field = 'publish_date'
    template_name = 'countries/pest_report_hidden_list.html'
    queryset = PestReport.objects.all().order_by('-publish_date', 'title')
    allow_future = False
    allow_empty = True
    paginate_by = 30

    def get_queryset(self):
        """ only return pest reports from the specific country """
        # self.country = get_object_or_404(CountryPage, country=self.kwargs['country'])
        self.country = self.kwargs['country']
        # CountryPage country_slug == country URL parameter keyword argument
        return PestReport.objects.filter(country__country_slug=self.country, status=CONTENT_STATUS_DRAFT)
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(PestReportHiddenListView, self).get_context_data(**kwargs)
        context['country'] = self.kwargs['country']
        # context.update({
        #     'country': self.kwargs['country']
        # })
        return context

    # put class-based generic view behind login
    # https://docs.djangoproject.com/en/dev/topics/class-based-views/intro/#decorating-the-class
    @method_decorator(login_required)
    @method_decorator(permission_required('ippc.add_pestreport', login_url="/accounts/login/"))
    def dispatch(self, *args, **kwargs):
        return super(PestReportHiddenListView, self).dispatch(*args, **kwargs)



class PestReportDetailView(DetailView):
    """ Pest report detail page """
    model = PestReport
    context_object_name = 'report'
    template_name = 'countries/pest_report_detail.html'
    queryset = PestReport.objects.filter(status=CONTENT_STATUS_PUBLISHED)

class PublicationListView(ListView):
    """
    Publications List
    """
    context_object_name = 'latest'
    model = Publication
    date_field = 'modify_date'
    template_name = 'pages/publication_list.html'
    queryset = Publication.objects.filter(status=IS_PUBLIC).order_by('-modify_date', 'title')
    allow_future = False
    allow_empty = True
    paginate_by = 50

class PublicationDetailView(DetailView):
    """ Publication detail page """
    model = Publication
    context_object_name = 'publication'
    template_name = 'pages/publication_detail.html'
    queryset = Publication.objects.filter(status=IS_PUBLIC)
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(PublicationDetailView, self).get_context_data(**kwargs)
        publication = get_object_or_404(Publication, id=self.kwargs['pk'])
    
        publicationlibrary = get_object_or_404(PublicationLibrary, id=publication.library_id)
        context['users'] =publicationlibrary.users
        context['groups'] = publicationlibrary.groups
        context['login_required'] = publicationlibrary.login_required
        return context
class PublicationDetail2View(DetailView):
    """ Publication detail page """
    model = Publication
    context_object_name = 'publication'
    template_name = 'pages/publication_detail.html'
    queryset = Publication.objects.filter(status=IS_PUBLIC)
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(PublicationDetail2View, self).get_context_data(**kwargs)
        publication = get_object_or_404(Publication, slug=self.kwargs['slug'])
    
        publicationlibrary = get_object_or_404(PublicationLibrary, id=publication.library_id)
        context['users'] =publicationlibrary.users
        context['groups'] = publicationlibrary.groups
        context['login_required'] = publicationlibrary.login_required
        return context
    
import os
import shutil

import zipfile
import StringIO
from settings import PROJECT_ROOT, MEDIA_ROOT
from django.core.files.storage import default_storage

class PublicationFilesListView(ListView):
    """
    Publications Files List
    """
    context_object_name = 'latest'
    model = Publication
    date_field = 'modify_date'
    template_name = 'pages/publicationfilestable.html'
    queryset = Publication.objects.filter(status=IS_PUBLIC).order_by('-modify_date', 'title')
    allow_future = False
    allow_empty = True
    paginate_by = 30
 
    def get_context_data(self, **kwargs):
        context = super(PublicationFilesListView, self).get_context_data(**kwargs)
        queryset = Publication.objects.filter(status=IS_PUBLIC,library_id=self.kwargs['id']).order_by('-modify_date', 'title')
        queryset2 = PublicationLibrary.objects.filter(id=self.kwargs['id'])
        for p in queryset2:
            context['titlepage']=p.title
        filenames_all=[]
        filenames_en=[]
        filenames_es=[]
        filenames_fr=[]
        filenames_ar=[]
        filenames_ru=[]
        filenames_zh=[]
        
        langs=[]
        langs.append(["en",filenames_en])
        langs.append(["es",filenames_es])
        langs.append(["fr",filenames_fr])
        langs.append(["ar",filenames_ar])
        langs.append(["ru",filenames_ru])
        langs.append(["zh",filenames_zh])
        
        for p in queryset:
            user_g=self.request.user.groups
            pub_g=p.groups
            if pub_g.all():
                for pg in pub_g.all():
                    if pg in user_g.all():
                        break;
                    else:
                        filenames_all.append(p.file_en)
                        filenames_all.append(p.file_es)
                        filenames_all.append(p.file_fr)
                        filenames_all.append(p.file_ru)
                        filenames_all.append(p.file_zh)
                        filenames_all.append(p.file_ar)
                        filenames_en.append(p.file_en)
                        filenames_es.append(p.file_es)
                        filenames_fr.append(p.file_fr)
                        filenames_ar.append(p.file_ar)
                        filenames_ru.append(p.file_ru)
                        filenames_zh.append(p.file_zh)
            else:
                filenames_all.append(p.file_en)
                filenames_all.append(p.file_es)
                filenames_all.append(p.file_fr)
                filenames_all.append(p.file_ru)
                filenames_all.append(p.file_zh)
                filenames_all.append(p.file_ar)
                filenames_en.append(p.file_en)
                filenames_es.append(p.file_es)
                filenames_fr.append(p.file_fr)
                filenames_ar.append(p.file_ar)
                filenames_ru.append(p.file_ru)
                filenames_zh.append(p.file_zh)             

            
        
        # The zip compressor
        date = timezone.now().strftime('%Y%m%d%H%M%S')+"_"+str(self.kwargs['id'])
        zip_all1 ="/static/media/tmp/"+"archive_all_"+ date+".zip"
        zip_all = zipfile.ZipFile(MEDIA_ROOT+"/tmp/"+"archive_all_"+ date+".zip", "w")
        for lang in langs:
            zip_lang1 = "/static/media/tmp/"+"archive_"+str(lang[0])+"_"+ date+".zip"
            zip_lang = zipfile.ZipFile(MEDIA_ROOT+"/tmp/"+"archive_"+str(lang[0])+"_"+ date+".zip", "w")
            for file_path in lang[1]:
                strfpath=os.path.join('/work/projects/ippcdj-env/public/', '/work/projects/ippcdj-env/public/static/media/')+str(file_path)
                filename = strfpath.split('/');
                fname=filename[len(filename)-1]
                zip_lang.write(strfpath, fname)
                zip_all.write(strfpath, fname)
            
            zip_lang.close()
            context['zip_'+str(lang[0])]=zip_lang1
            size=os.path.getsize(zip_lang.filename)
            if size >182:
                context['zip_'+str(lang[0])+'_s']=os.path.getsize(zip_lang.filename)
        
        zip_all.close()
        
        context['zip_all']=zip_all1
        context['zip_all_s']=os.path.getsize(zip_all.filename)
        
        destination = '/work/projects/ippcdj-env/public/static/media/tmp/'
        src_files = os.listdir(MEDIA_ROOT+"/tmp/")
        for file_name in src_files:
            full_file_name = os.path.join(MEDIA_ROOT+"/tmp/", file_name)
            #if (os.path.isfile(full_file_name)):
            #     shutil.move(full_file_name, destination)
        source = MEDIA_ROOT+"/tmp/"
        
        return context
            
            
            
def send_notification_message(newitem,id,content_type,title,url):
    """ send_notification_message """
    notify_instance = get_object_or_404(NotificationMessageRelate, object_id=id,content_type__pk=content_type.id,)
    
    if notify_instance.notify:
        #print("send!!!")
        emailto_all = ['']
        for cn in notify_instance.countries.all():
            countryo = get_object_or_404(CountryPage, page_ptr_id=cn.id)
            user_obj=User.objects.get(id=countryo.contact_point_id)
            emailto_all.append(str(user_obj.email))
        for partner in notify_instance.partners.all():
            countryo = get_object_or_404(PartnersPage, page_ptr_id=partner.id)
            user_obj=User.objects.get(id=countryo.contact_point_id)
            emailto_all.append(str(user_obj.email))
        if notify_instance.notifysecretariat :
            #print("sec!!!")
            emailto_all.append(str('ippc@fao.org'))
        print(emailto_all)
        subject=''
        if newitem==1:
            subject='ADDED new content: ' +title
        else:    
            subject='UPDATE to: ' +title
        itemllink="https://www.ippc.int/countries/"+url
        textmessage ='<table bgcolor="#FFFFFF" cellspacing="2" cellpadding="2" valign="top" width="100%" style="border-bottom: 1px solid #10501F;border-top: 1px solid #10501F;border-left: 1px solid #10501F;border-right: 1px solid #10501F"> <tr><td width="100%" bgcolor="#FFFFFF">Please be informed that the following information has been added/updated on the <b>International Phytosanitary Portal:</b><br>'+title+' ('+itemllink+')</td></tr><tr bgcolor="#FFFFFF"><td bgcolor="#FFFFFF"></td></tr><tr><td width="100%" bgcolor="#FFFFFF">If you no longer wish to receive these notifications, please notify this country\'s IPPC Contact Point.</td></tr></table>'
        
        #message = mail.EmailMessage(subject,textmessage,'paola.sentinelli@fao.org',#from
        #    ['paola.sentinelli@fao.org',], ['paola.sentinelli@fao.org'])#emailto_all for PROD, in TEST all to paola#
        message = mail.EmailMessage(subject,textmessage,'ippc@fao.org',#from
            emailto_all, ['paola.sentinelli@fao.org'])#emailto_all for PROD, in TEST all to paola#
        print(textmessage)
        message.content_subtype = "html"
        sent =message.send()
   
 
@login_required
@permission_required('ippc.add_pestreport', login_url="/accounts/login/")
def pest_report_create(request, country):
    """ Create Pest Report """
    user = request.user
    author = user
    country=user.get_profile().country
    user_country_slug = lower(slugify(country))

    form = PestReportForm(request.POST, request.FILES)
    issueform =IssueKeywordsRelateForm(request.POST)
    commodityform =CommodityKeywordsRelateForm(request.POST)
    notifyrelateform =NotificationMessageRelateForm(request.POST)
        
    countryo = get_object_or_404(CountryPage, name=country)
    numberR=PestReport.objects.filter(country__country_slug=country).count()
    numberR=numberR+1
    pestnumber=str(numberR)
    if numberR<10 :
        pestnumber='0'+pestnumber
    report_number_val=countryo.iso3+'-'+pestnumber+'/1'
    #print   (report_number_val)     
   
    if request.method == "POST":
         f_form = PestReportFileFormSet(request.POST, request.FILES)
         u_form = PestReportUrlFormSet(request.POST)
         if form.is_valid() and f_form.is_valid() and u_form.is_valid():
            new_pest_report = form.save(commit=False)
            new_pest_report.author = request.user
            new_pest_report.report_number=report_number_val
            new_pest_report.author_id = author.id
            form.save()
           
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = new_pest_report
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = new_pest_report
            commodity_instance.save()
            commodityform.save_m2m()
            
            notify_instance = notifyrelateform.save(commit=False)
            notify_instance.content_object = new_pest_report
            notify_instance.save()
            notifyrelateform.save_m2m()
            
            f_form.instance = new_pest_report
            f_form.save()
            u_form.instance = new_pest_report
            u_form.save()
            content_type = ContentType.objects.get_for_model(new_pest_report)
       
            send_notification_message(1,new_pest_report.id,content_type,new_pest_report.title,user_country_slug+'/pestreports/'+str(new_pest_report.publish_date.strftime("%Y"))+'/'+str(new_pest_report.publish_date.strftime("%m"))+'/'+new_pest_report.slug+'/')
            
            info(request, _("Successfully created pest report."))
            
            if new_pest_report.status == CONTENT_STATUS_DRAFT:
                return redirect("pest-report-hidden-list", country=user_country_slug)
            else:
                return redirect("pest-report-detail", country=user_country_slug, year=new_pest_report.publish_date.strftime("%Y"), month=new_pest_report.publish_date.strftime("%m"), slug=new_pest_report.slug)
         else:
             return render_to_response('countries/pest_report_create.html', {'form': form,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform,'notifyrelateform':notifyrelateform},
             context_instance=RequestContext(request))
       
    else:
        form = PestReportForm(initial={'country': country}, instance=PestReport())
        issueform =IssueKeywordsRelateForm(request.POST)
        commodityform =CommodityKeywordsRelateForm(request.POST)
        notifyrelateform =NotificationMessageRelateForm(request.POST)
   
        f_form =PestReportFileFormSet()
        u_form =PestReportUrlFormSet()
    return render_to_response('countries/pest_report_create.html', {'form': form,'f_form': f_form,'u_form':u_form,'issueform':issueform, 'commodityform':commodityform,'notifyrelateform':notifyrelateform},
        context_instance=RequestContext(request))


# http://stackoverflow.com/a/1854453/412329
@login_required
@permission_required('ippc.change_pestreport', login_url="/accounts/login/")
def pest_report_edit(request, country, id=None, template_name='countries/pest_report_edit.html'):
    """ Edit Pest Report """
    user = request.user
    author = user
    country = user.get_profile().country
    # country_id = PestReport.objects.filter(country__country_id=country.id)
    user_country_slug = lower(slugify(country))
    
    
    
    if id:
        pest_report = get_object_or_404(PestReport, country=country, pk=id)
       
        content_type = ContentType.objects.get_for_model(pest_report)
        notifications = get_object_or_404(NotificationMessageRelate, object_id=id,content_type__pk=content_type.id)
        
        rep_num=pest_report.report_number
        indexof=rep_num.rfind('/')
        numberRep_part=rep_num[:indexof+1]
        numberRep=int(rep_num[indexof+1:])+1
        pest_report.report_number=numberRep_part+str(numberRep)
       # if pest_report.author != request.user:
        #     return HttpResponseForbidden()
    else:
        pest_report = PestReport(author=request.user)

    if request.POST:
        form = PestReportForm(request.POST,  request.FILES, instance=pest_report)
        if pest_report.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=pest_report.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm(request.POST,instance=issues)
        else:
            issueform =IssueKeywordsRelateForm(request.POST)
        if pest_report.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=pest_report.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm(request.POST,instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm(request.POST)
        notifyrelateform =NotificationMessageRelateForm(request.POST,instance=notifications)
        f_form = PestReportFileFormSet(request.POST,  request.FILES,instance=pest_report)
        u_form =PestReportUrlFormSet(request.POST,  instance=pest_report)
        if form.is_valid() and f_form.is_valid() and u_form.is_valid():
            form.save()
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = pest_report
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = pest_report
            commodity_instance.save()
            commodityform.save_m2m() 
            
            notify_instance = notifyrelateform.save(commit=False)
            notify_instance.content_object = pest_report
            notify_instance.save()
            notifyrelateform.save_m2m()
            
            f_form.instance = pest_report
            f_form.save()
            u_form.instance = pest_report
            u_form.save()
            send_notification_message(0,id,content_type,pest_report.title,user_country_slug+'/pestreports/'+str(pest_report.publish_date.strftime("%Y"))+'/'+str(pest_report.publish_date.strftime("%m"))+'/'+pest_report.slug+'/')
            
            # If the save was successful, success message and redirect to another page
            # info(request, _("Successfully updated pest report."))
            if pest_report.status == CONTENT_STATUS_DRAFT:
                return redirect("pest-report-hidden-list", country=user_country_slug)
            else:
                return redirect("pest-report-detail",country=user_country_slug, year=pest_report.publish_date.strftime("%Y"), month=pest_report.publish_date.strftime("%m"), slug=pest_report.slug)

    else:
        form = PestReportForm(instance=pest_report)
        if pest_report.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=pest_report.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm( instance=issues)
        else:
            issueform =IssueKeywordsRelateForm( )
        if pest_report.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=pest_report.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm( instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm()
        notifyrelateform =NotificationMessageRelateForm(instance=notifications)
        f_form = PestReportFileFormSet(instance=pest_report)
        u_form = PestReportUrlFormSet(instance=pest_report)
    return render_to_response(template_name, {
        'form': form,'f_form':f_form,'u_form':u_form,'issueform': issueform,'commodityform': commodityform,  "pest_report": pest_report,'notifyrelateform':notifyrelateform
    }, context_instance=RequestContext(request))

class ReportingObligationListView(ListView):
    """    Reporting Obligation """
    context_object_name = 'latest'
    model = ReportingObligation
    date_field = 'publish_date'
    template_name = 'countries/reporting_obligation_list.html'
    queryset = ReportingObligation.objects.all().order_by('-publish_date', 'title')
    
    allow_future = False
    allow_empty = True
    paginate_by = 30

    def get_queryset(self):
        """ only return pest reports from the specific country """
        # self.country = get_object_or_404(CountryPage, country=self.kwargs['country'])
        self.country = self.kwargs['country']
        self.type = self.kwargs['type']
        # CountryPage country_slug == country URL parameter keyword argument
        return ReportingObligation.objects.filter(country__country_slug=self.country,reporting_obligation_type=self.kwargs['type'])
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(ReportingObligationListView, self).get_context_data(**kwargs)
        context['country'] = self.kwargs['country']
        context['basic_types'] =BASIC_REP_TYPE_CHOICES
        context['current_type'] =int(self.kwargs['type'])
        return context
   
   
 

   
   
   
   
class IppcUserProfileDetailView(DetailView):
    """  Profile """
    model = IppcUserProfile
    context_object_name = 'user'
    template_name = 'accounts/account_profile.html'
    queryset = IppcUserProfile.objects.filter()


@login_required
def profile_update(request, template="accounts/account_profile_update.html"):
    """
    Profile update form.
    """
    profile_form = get_profile_form()
    form = profile_form(request.POST or None, request.FILES or None,
                        instance=request.user)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        info(request, _("Profile updated"))
        try:
            return redirect("profile", username=user.username)
        except NoReverseMatch:
            return redirect("profile_update")
    context = {"form": form, "title": _("Update Profile")}
    return render(request, template, context)

# http://stackoverflow.com/a/1854453/412329
# @login_required
# def profile_update(request ,id=None, template_name='accounts/account_profile_update.html'):
#     """ Edit Profile """
#     user = request.user
#
#     if id:
#         profile = get_object_or_404(IppcUserProfile, pk=id)
#         userprofile = get_object_or_404(User, pk=profile.user_id)
#     if request.POST:
#         form = IppcUserProfileForm(request.POST,   instance=profile)
#         userform = UserForm(request.POST, instance=request.user)
#         if form.is_valid() and userform.is_valid():
#             form.save()
#             userform.save()
#             return redirect("user-detail",id)
#     else:
#         form = IppcUserProfileForm(instance=profile)
#         userform = UserForm(request.POST, instance=request.user)
#
#     return render_to_response(template_name, {
#         'form': form, 'userform': userform,'email':request.user.email,
#     }, context_instance=RequestContext(request))
       
   
class ReportingObligationDetailView(DetailView):
    """  Reporting Obligation detail page """
    model = ReportingObligation
    context_object_name = 'reportingobligation'
    template_name = 'countries/reporting_obligation_detail.html'
    queryset = ReportingObligation.objects.filter()


@login_required
@permission_required('ippc.add_reportingobligation', login_url="/accounts/login/")
def reporting_obligation_create(request, country,type):
    """ Create Reporting Obligation """
    user = request.user
    author = user
    country=user.get_profile().country
    user_country_slug = lower(slugify(country))

    form = ReportingObligationForm(request.POST, request.FILES)
    issueform =IssueKeywordsRelateForm(request.POST)
    commodityform =CommodityKeywordsRelateForm(request.POST)
    notifyrelateform =NotificationMessageRelateForm(request.POST)
     
    if request.method == "POST":
         f_form = ReportingoblicationFileFormSet(request.POST, request.FILES)
         u_form = ReportingObligationUrlFormSet(request.POST)
         if form.is_valid() and f_form.is_valid() and u_form.is_valid():
            new_reporting_obligation = form.save(commit=False)
            new_reporting_obligation.author = request.user
            new_reporting_obligation.author_id = author.id
            new_reporting_obligation.report_obligation_type = type
            form.save()
            
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = new_reporting_obligation
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = new_reporting_obligation
            commodity_instance.save()
            commodityform.save_m2m()
            
            notify_instance = notifyrelateform.save(commit=False)
            notify_instance.content_object = new_reporting_obligation
            notify_instance.save()
            notifyrelateform.save_m2m()
            
            f_form.instance = new_reporting_obligation
            f_form.save()
            u_form.instance = new_reporting_obligation
            u_form.save()
            
            content_type = ContentType.objects.get_for_model(new_reporting_obligation)
       
            send_notification_message(1,new_reporting_obligation.id,content_type,new_reporting_obligation.title,user_country_slug+'/reportingobligation/'+str(new_reporting_obligation.publish_date.strftime("%Y"))+'/'+str(new_reporting_obligation.publish_date.strftime("%m"))+'/'+new_reporting_obligation.slug+'/')
            
            info(request, _("Successfully created Reporting obligation."))
            return redirect("reporting-obligation-detail", country=user_country_slug, year=new_reporting_obligation.publish_date.strftime("%Y"), month=new_reporting_obligation.publish_date.strftime("%m"), slug=new_reporting_obligation.slug)
         else:
            return render_to_response('countries/reporting_obligation_create.html', {'form': form,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform,'notifyrelateform':notifyrelateform},
             context_instance=RequestContext(request))
    else:
        form = ReportingObligationForm(initial={'country': country,'reporting_obligation_type': type}, instance=ReportingObligation())
        issueform =IssueKeywordsRelateForm(request.POST)
        commodityform =CommodityKeywordsRelateForm(request.POST)
        notifyrelateform =NotificationMessageRelateForm(request.POST)
        f_form =ReportingoblicationFileFormSet()
        u_form =ReportingObligationUrlFormSet()

    return render_to_response('countries/reporting_obligation_create.html', {'form': form  ,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform,'notifyrelateform':notifyrelateform},
        context_instance=RequestContext(request))
        
        
        
# http://stackoverflow.com/a/1854453/412329
@login_required
@permission_required('ippc.change_reportingobligation', login_url="/accounts/login/")
def reporting_obligation_edit(request, country, id=None, template_name='countries/reporting_obligation_edit.html'):
    """ Edit Reporting Obligation """
    user = request.user
    author = user
    country = user.get_profile().country
    # country_id = PestReport.objects.filter(country__country_id=country.id)
    user_country_slug = lower(slugify(country))
    if id:
        reporting_obligation = get_object_or_404(ReportingObligation, country=country, pk=id)
        content_type = ContentType.objects.get_for_model(reporting_obligation)
        try:
            notifications = get_object_or_404(NotificationMessageRelate, object_id=id,content_type__pk=content_type.id)
        except:
            notifications = None
    else:
        reporting_obligation = ReportingObligation(author=request.user)
      
    if request.POST:
        form = ReportingObligationForm(request.POST, request.FILES, instance=reporting_obligation)
        if reporting_obligation.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=reporting_obligation.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm(request.POST,instance=issues)
        else:
            issueform =IssueKeywordsRelateForm(request.POST)
        if reporting_obligation.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=reporting_obligation.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm(request.POST,instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm(request.POST)
        notifyrelateform =NotificationMessageRelateForm(request.POST,instance=notifications)
        f_form = ReportingoblicationFileFormSet(request.POST,  request.FILES,instance=reporting_obligation)
        u_form =ReportingObligationUrlFormSet(request.POST,instance=reporting_obligation)
        if form.is_valid() and f_form.is_valid() and u_form.is_valid():
            form.save()
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = reporting_obligation
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = reporting_obligation
            commodity_instance.save()
            commodityform.save_m2m() 
            
            notify_instance = notifyrelateform.save(commit=False)
            notify_instance.content_object = reporting_obligation
            notify_instance.save()
            notifyrelateform.save_m2m()
            
            f_form.instance = reporting_obligation
            f_form.save()
            u_form.instance = reporting_obligation
            u_form.save()
            # If the save was successful, success message and redirect to another page
            send_notification_message(0,id,content_type,reporting_obligation.title,user_country_slug+'/reportingobligation/'+str(reporting_obligation.publish_date.strftime("%Y"))+'/'+str(reporting_obligation.publish_date.strftime("%m"))+'/'+reporting_obligation.slug+'/')
            
            info(request, _("Successfully updated Reporting obligation."))
            return redirect("reporting-obligation-detail", country=user_country_slug, year=reporting_obligation.publish_date.strftime("%Y"), month=reporting_obligation.publish_date.strftime("%m"), slug=reporting_obligation.slug)

    else:
        form = ReportingObligationForm(instance=reporting_obligation)
        if reporting_obligation.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=reporting_obligation.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm( instance=issues)
        else:
            issueform =IssueKeywordsRelateForm( )
        if reporting_obligation.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=reporting_obligation.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm( instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm()
        notifyrelateform =NotificationMessageRelateForm(instance=notifications)
        f_form = ReportingoblicationFileFormSet(instance=reporting_obligation)
        u_form = ReportingObligationUrlFormSet(instance=reporting_obligation)
    return render_to_response(template_name, {
        'form': form,'f_form':f_form,'u_form': u_form,'issueform': issueform,'commodityform': commodityform,  "reporting_obligation": reporting_obligation,'notifyrelateform':notifyrelateform
    }, context_instance=RequestContext(request))


class EventReportingListView(ListView):
    """    Event Reporting """
    context_object_name = 'latest'
    model = EventReporting
    date_field = 'publish_date'
    template_name = 'countries/event_reporting_list.html'
    queryset = EventReporting.objects.all().order_by('-publish_date', 'title')
    
    allow_future = False
    allow_empty = True
    paginate_by = 30

    def get_queryset(self):
        """ only return pest reports from the specific country """
        # self.country = get_object_or_404(CountryPage, country=self.kwargs['country'])
        self.country = self.kwargs['country']
        self.type = self.kwargs['type']
        # CountryPage country_slug == country URL parameter keyword argument
        return EventReporting.objects.filter(country__country_slug=self.country,event_rep_type=self.kwargs['type'])
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(EventReportingListView, self).get_context_data(**kwargs)
        context['country'] = self.kwargs['country']
        context['event_types'] =EVT_REP_TYPE_CHOICES
        context['current_type'] =int(self.kwargs['type'])
        return context
   
       
   
class EventReportingDetailView(DetailView):
    """ EventReporting detail page """
    model = EventReporting
    context_object_name = 'eventreporting'
    template_name = 'countries/eventreporting_detail.html'
    queryset = EventReporting.objects.filter()



@login_required
@permission_required('ippc.add_eventreporting', login_url="/accounts/login/")
def event_reporting_create(request, country,type):
    """ Create Event Reporting """
    user = request.user
    author = user
    country=user.get_profile().country
    user_country_slug = lower(slugify(country))


    form = EventReportingForm(request.POST or None, request.FILES)
    issueform =IssueKeywordsRelateForm(request.POST)
    commodityform =CommodityKeywordsRelateForm(request.POST)
    notifyrelateform =NotificationMessageRelateForm(request.POST)
    
    if request.method == "POST":
        f_form = EventreportingFileFormSet(request.POST, request.FILES)
        u_form = EventreportingUrlFormSet(request.POST)
        if form.is_valid() and f_form.is_valid() and u_form.is_valid():
            new_event_reporting = form.save(commit=False)
            new_event_reporting.author = request.user
            new_event_reporting.author_id = author.id
            new_event_reporting.event_rep_type = type
            form.save()
            
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = new_event_reporting
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = new_event_reporting
            commodity_instance.save()
            commodityform.save_m2m()      
            
            notification_instance = notifyrelateform.save(commit=False)
            notification_instance.content_object = new_event_reporting
            notification_instance.save()
            notifyrelateform.save_m2m()
            
            f_form.instance = new_event_reporting
            f_form.save()
            u_form.instance = new_event_reporting
            u_form.save()
            content_type = ContentType.objects.get_for_model(new_event_reporting)
            send_notification_message(1,new_event_reporting.id,content_type,new_event_reporting.title,user_country_slug+'/eventreporting/'+str(new_event_reporting.publish_date.strftime("%Y"))+'/'+str(new_event_reporting.publish_date.strftime("%m"))+'/'+new_event_reporting.slug+'/')
            info(request, _("Successfully added Event reporting."))
            return redirect("event-reporting-detail", country=user_country_slug, year=new_event_reporting.publish_date.strftime("%Y"), month=new_event_reporting.publish_date.strftime("%m"), slug=new_event_reporting.slug)
        else:
            return render_to_response('countries/event_reporting_create.html', {'form': form,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform,'notifyrelateform': notifyrelateform,},#'docform':myformset,
             context_instance=RequestContext(request))

          
        
    else:
        form = EventReportingForm(initial={'country': country,'event_rep_type': type}, instance=EventReporting())
        issueform =IssueKeywordsRelateForm(request.POST)
        commodityform =CommodityKeywordsRelateForm(request.POST)
        notifyrelateform =NotificationMessageRelateForm(request.POST)
        f_form = EventreportingFileFormSet()
        u_form = EventreportingUrlFormSet()
    
    return render_to_response('countries/event_reporting_create.html', {'form': form,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform,'notifyrelateform': notifyrelateform,},
        context_instance=RequestContext(request))

        

@login_required
@permission_required('ippc.change_eventreporting', login_url="/accounts/login/")
def event_reporting_edit(request, country, id=None, template_name='countries/event_reporting_edit.html'):
    """ Edit  Reporting """
    user = request.user
    author = user
    country = user.get_profile().country
    # country_id = PestReport.objects.filter(country__country_id=country.id)
    user_country_slug = lower(slugify(country))
    if id:
        event_reporting = get_object_or_404(EventReporting, country=country, pk=id)
        content_type = ContentType.objects.get_for_model(event_reporting)
        try:
            notifications = get_object_or_404(NotificationMessageRelate, object_id=id,content_type__pk=content_type.id)
        except:
            notifications = None
    else:
        event_reporting = EventReporting(author=request.user)
      
    if request.POST:
        form = EventReportingForm(request.POST,  request.FILES, instance=event_reporting)
        if event_reporting.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=event_reporting.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm(request.POST,instance=issues)
        else:
            issueform =IssueKeywordsRelateForm(request.POST)
        if event_reporting.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=event_reporting.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm(request.POST,instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm(request.POST)
            
        notifyrelateform =NotificationMessageRelateForm(request.POST,instance=notifications)
        f_form = EventreportingFileFormSet(request.POST,  request.FILES,instance=event_reporting)
        u_form = EventreportingUrlFormSet(request.POST,  instance=event_reporting)
      
        if form.is_valid() and f_form.is_valid() and u_form.is_valid():
            form.save()
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = event_reporting
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = event_reporting
            commodity_instance.save()
            commodityform.save_m2m() 
       
            notification_instance = notifyrelateform.save(commit=False)
            notification_instance.content_object = event_reporting
            notification_instance.save()
            notifyrelateform.save_m2m()
            
            f_form.instance = event_reporting
            f_form.save()
            u_form.instance = event_reporting
            u_form.save()
            send_notification_message(0,id,content_type,event_reporting.title,user_country_slug+'/eventreporting/'+str(event_reporting.publish_date.strftime("%Y"))+'/'+str(event_reporting.publish_date.strftime("%m"))+'/'+event_reporting.slug+'/')
            
            info(request, _("Successfully updated Event reporting."))
            return redirect("event-reporting-detail", country=user_country_slug, year=event_reporting.publish_date.strftime("%Y"), month=event_reporting.publish_date.strftime("%m"), slug=event_reporting.slug)

    else:
        form = EventReportingForm(instance=event_reporting)
        if event_reporting.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=event_reporting.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm( instance=issues)
        else:
            issueform =IssueKeywordsRelateForm( )
        if event_reporting.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=event_reporting.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm( instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm()
        notifyrelateform =NotificationMessageRelateForm(instance=notifications)
        f_form = EventreportingFileFormSet(instance=event_reporting)
        u_form = EventreportingUrlFormSet( instance=event_reporting)
      
    return render_to_response(template_name, {
        'form': form, 'f_form':f_form,'u_form': u_form,'issueform': issueform,  'commodityform': commodityform, "event_reporting": event_reporting,'notifyrelateform':notifyrelateform
    }, context_instance=RequestContext(request))
    


class DraftProtocolListView(ListView):
    """    DraftProtocol """
    context_object_name = 'latest'
    model = DraftProtocol
    date_field = 'publish_date'
    template_name = 'dp/dp_list.html'
    queryset = DraftProtocol.objects.all().order_by('-publish_date', 'title')
    
    allow_future = False
    allow_empty = True
    paginate_by = 30

class DraftProtocolDetailView(DetailView):
    """ DraftProtocol detail page """
    model = DraftProtocol
    context_object_name = 'draftprotocol'
    template_name = 'dp/dp_detail.html'
    queryset = DraftProtocol.objects.filter()

    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(DraftProtocolDetailView, self).get_context_data(**kwargs)
        draftprotocol = get_object_or_404(DraftProtocol,  slug=self.kwargs['slug'])
        queryset = DraftProtocolComments.objects.filter(draftprotocol_id=draftprotocol.id)
        add_comment= 1
        see_all_comment= 0
        
        for obj in queryset:
           if self.request.user == obj.author:
                  add_comment=0
        if self.request.user.groups.filter(name='IPPC Secretariat') or self.request.user.groups.filter(name='TPDPc') :
            see_all_comment=1
        
         
        context['comments'] =queryset
        context['see_all_comment'] =see_all_comment
        context['add_comment'] =add_comment
        return context

@login_required
@permission_required('ippc.add_publication', login_url="/accounts/login/")
def draftprotocol_create(request):
    """ Create DraftProtocol """
    user = request.user
    author = user


    form = DraftProtocolForm(request.POST or None, request.FILES)
     
    if request.method == "POST":
        f_form = DraftProtocolFileFormSet(request.POST, request.FILES)
        if form.is_valid() and f_form.is_valid() :
            new_draftprotocol = form.save(commit=False)
            new_draftprotocol.author = request.user
            new_draftprotocol.author_id = author.id
            form.save()
            
            f_form.instance = new_draftprotocol
            f_form.save()
           
            info(request, _("Successfully added Draft Protocol."))
            return redirect("draftprotocol-detail",  year=new_draftprotocol.publish_date.strftime("%Y"), month=new_draftprotocol.publish_date.strftime("%m"), slug=new_draftprotocol.slug)
        else:
            return render_to_response('dp/dp_create.html', {'form': form,'f_form': f_form,},#'entryform': entryform,'docform':myformset,
             context_instance=RequestContext(request))

          
        
    else:
        form = DraftProtocolForm(instance=DraftProtocol())
        f_form =DraftProtocolFileFormSet()
      
    return render_to_response('dp/dp_create.html', {'form': form,'f_form': f_form,},
        context_instance=RequestContext(request))

        

@login_required
@permission_required('ippc.add_publication', login_url="/accounts/login/")
def draftprotocol_edit(request, id=None, template_name='dp/dp_edit.html'):
    """ DraftProtocol """
    user = request.user
    author = user
    if id:
        draftprotocol = get_object_or_404(DraftProtocol,  pk=id)
    else:
        draftprotocol = DraftProtocol(author=request.user)
      
    if request.POST:
        form = DraftProtocolForm(request.POST,  request.FILES, instance=draftprotocol)
        f_form = DraftProtocolFileFormSet(request.POST,  request.FILES,instance=draftprotocol)

      
        if form.is_valid() and f_form.is_valid():
            form.save()
            f_form.instance = draftprotocol
            f_form.save()
            info(request, _("Successfully updated DraftProtocol."))
            return redirect("draftprotocol-detail", year=draftprotocol.publish_date.strftime("%Y"), month=draftprotocol.publish_date.strftime("%m"), slug=draftprotocol.slug)

    else:
        form = DraftProtocolForm(instance=draftprotocol)
        f_form = DraftProtocolFileFormSet(instance=draftprotocol)
      
      
    return render_to_response(template_name, {
        'form': form, 'f_form':f_form, "draftprotocol": draftprotocol
    }, context_instance=RequestContext(request))
    



@login_required
@permission_required('ippc.add_draftcomment', login_url="/accounts/login/")
def draftprotocol_comment_create(request, id=None):
    """ Create  draftprotocol comment"""
    user = request.user
    author = user
    draftprotocol = get_object_or_404(DraftProtocol,  pk=id)
    form = DraftProtocolCommentsForm(request.POST or None, request.FILES)
     
    if request.method == "POST":
        if form.is_valid() :
            new_draftprotocolComment = form.save(commit=False)
            new_draftprotocolComment.author = request.user
            new_draftprotocolComment.author_id = author.id
            new_draftprotocolComment.title = request.user
            new_draftprotocolComment.draftprotocol_id = id
            
            form.save()
        
           
            info(request, _("Successfully added Comment."))
            return redirect("draftprotocol-detail",  year=draftprotocol.publish_date.strftime("%Y"), month=draftprotocol.publish_date.strftime("%m"), slug=draftprotocol.slug)
        else:
            return render_to_response('dp/dp_comment_create.html', {'form': form,},
             context_instance=RequestContext(request))
    else:
        form = DraftProtocolCommentsForm(initial={'draftprotocol': id},instance=DraftProtocolComments())
      
    return render_to_response('dp/dp_comment_create.html', {'form': form,'draftprotocol': id,},
        context_instance=RequestContext(request))

        

@login_required
@permission_required('ippc.add_draftcomment', login_url="/accounts/login/")
def draftprotocol_comment_edit(request, id=None, dp_id=None, template_name='dp/dp_comment_edit.html'):
    """ DraftProtocol comment edit"""
    user = request.user
    author = user
    if id:
        draftprotocolcomment = get_object_or_404(DraftProtocolComments,  pk=id)
    else:
        draftprotocolcomment = DraftProtocolComments(author=request.user)
    
    draftprotocol = get_object_or_404(DraftProtocol,  pk=dp_id)
        
      
    if request.POST:
        form = DraftProtocolCommentsForm(request.POST,  request.FILES, instance=draftprotocolcomment)
        if form.is_valid() :
            form.save()
            f_form.instance = draftprotocolcomment
            f_form.save()
            info(request, _("Successfully updated DraftProtocol."))
            return redirect("draftprotocol-detail", year=draftprotocol.publish_date.strftime("%Y"), month=draftprotocol.publish_date.strftime("%m"), slug=draftprotocol.slug)

    else:
        form = DraftProtocolCommentsForm(instance=draftprotocolcomment)
        
      
      
    return render_to_response(template_name, {
        'form': form,  "draftprotocolcomment": draftprotocolcomment
    }, context_instance=RequestContext(request))
    



class WebsiteListView(ListView):
    """ Website """
    context_object_name = 'latest'
    model = Website
    date_field = 'publish_date'
    template_name = 'countries/website_list.html'
    queryset = Website.objects.all().order_by('-publish_date', 'title')
    
    allow_future = False
    allow_empty = True
    paginate_by = 30

    def get_queryset(self):
        """ only return Website from the specific country """
        # self.country = get_object_or_404(CountryPage, country=self.kwargs['country'])
        self.country = self.kwargs['country']
        # CountryPage country_slug == country URL parameter keyword argument
        return Website.objects.filter(country__country_slug=self.country)
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(WebsiteListView, self).get_context_data(**kwargs)
        context['country'] = self.kwargs['country']
        return context
   
       
   
class WebsiteDetailView(DetailView):
    """ EventReporting detail page """
    model = Website
    context_object_name = 'website'
    template_name = 'countries/website_detail.html'
    queryset = Website.objects.filter()



@login_required
@permission_required('ippc.add_website', login_url="/accounts/login/")
def website_create(request, country):
    """ Create website """
    user = request.user
    author = user
    country=user.get_profile().country
    user_country_slug = lower(slugify(country))

    form = WebsiteForm(request.POST or None, request.FILES)
    issueform =IssueKeywordsRelateForm(request.POST)
    commodityform =CommodityKeywordsRelateForm(request.POST)
    
         
    if request.method == "POST":
        u_form =WebsiteUrlFormSet(request.POST)
        if form.is_valid() and u_form.is_valid():
            new_website = form.save(commit=False)
            new_website.author = request.user
            new_website.author_id = author.id
            form.save()
            
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = new_website
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = new_website
            commodity_instance.save()
            commodityform.save_m2m()      
              
          
            u_form.instance = new_website
            u_form.save()
            info(request, _("Successfully added Website."))
            return redirect("website-detail", country=user_country_slug, year=new_website.publish_date.strftime("%Y"), month=new_website.publish_date.strftime("%m"), slug=new_website.slug)
        else:
            return render_to_response('countries/website_create.html', {'form': form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform},#'entryform': entryform,'docform':myformset,
             context_instance=RequestContext(request))

          
        
    else:
        form = WebsiteForm(initial={'country': country}, instance=Website())
        issueform =IssueKeywordsRelateForm(request.POST)
        commodityform =CommodityKeywordsRelateForm(request.POST)
        u_form = WebsiteUrlFormSet()
    
    return render_to_response('countries/website_create.html', {'form': form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform},
        context_instance=RequestContext(request))

        

@login_required
@permission_required('ippc.change_website', login_url="/accounts/login/")
def website_edit(request, country, id=None, template_name='countries/website_edit.html'):
    """ Edit  website """
    user = request.user
    author = user
    country = user.get_profile().country
    # country_id = PestReport.objects.filter(country__country_id=country.id)
    user_country_slug = lower(slugify(country))
    if id:
        website = get_object_or_404(Website, country=country, pk=id)
     
    else:
        website = Website(author=request.user)
      
    if request.POST:
        form = WebsiteForm(request.POST,  request.FILES, instance=website)
        if website.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=website.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm(request.POST,instance=issues)
        else:
            issueform =IssueKeywordsRelateForm(request.POST)
        if website.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=website.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm(request.POST,instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm(request.POST)
        u_form = WebsiteUrlFormSet(request.POST,  instance=website)
      
        if form.is_valid()  and u_form.is_valid():
            form.save()
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = website
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = website
            commodity_instance.save()
            commodityform.save_m2m() 
    
           
            u_form.instance = website
            u_form.save()
            info(request, _("Successfully updated Website."))
            return redirect("website-detail", country=user_country_slug, year=website.publish_date.strftime("%Y"), month=website.publish_date.strftime("%m"), slug=website.slug)

    else:
        form = WebsiteForm(instance=website)
        if website.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=website.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm( instance=issues)
        else:
            issueform =IssueKeywordsRelateForm( )
        if website.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=website.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm( instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm()
        u_form = WebsiteUrlFormSet( instance=website)
      
    return render_to_response(template_name, {
        'form': form, 'u_form': u_form,'issueform': issueform,  'commodityform': commodityform, "website": website
    }, context_instance=RequestContext(request))
    







class PartnersWebsiteDetailView(DetailView):
    """ EventReporting detail page """
    model = PartnersWebsite
    context_object_name = 'website'
    template_name = 'partners/website_detail.html'
    queryset = PartnersWebsite.objects.filter()

    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(PartnersWebsiteDetailView, self).get_context_data(**kwargs)
        page = get_object_or_404(PartnersPage, name=self.kwargs['partners'])
        context['pagetitle'] =  page.name
        context['pageslug'] =  page.slug
       # context['page'] =  page.partner_slug
        return context
     

@login_required
@permission_required('ippc.add_partnerswebsite', login_url="/accounts/login/")
def partner_websites_create(request, partner):
    """ Create website """
    user = request.user
    author = user
    partner=user.get_profile().partner
    user_partner_slug = lower(slugify(partner))

    form = PartnersWebsiteForm(request.POST or None, request.FILES)
    issueform =IssueKeywordsRelateForm(request.POST)
    commodityform =CommodityKeywordsRelateForm(request.POST)
    
         
    if request.method == "POST":
        u_form =PartnersWebsiteUrlFormSet(request.POST)
        if form.is_valid() and u_form.is_valid():
            new_website = form.save(commit=False)
            new_website.author = request.user
            new_website.author_id = author.id
            form.save()
            
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = new_website
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = new_website
            commodity_instance.save()
            commodityform.save_m2m()      
              
          
            u_form.instance = new_website
            u_form.save()
            info(request, _("Successfully added Website."))
            return redirect("partner-websites-detail", partners=user_partner_slug, year=new_website.publish_date.strftime("%Y"), month=new_website.publish_date.strftime("%m"), slug=new_website.slug)
        else:
            return render_to_response('partners/website_create.html', {'form': form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform},#'entryform': entryform,'docform':myformset,
             context_instance=RequestContext(request))

          
        
    else:
        form = PartnersWebsiteForm(initial={'partners': partner}, instance=PartnersWebsite())
        issueform =IssueKeywordsRelateForm(request.POST)
        commodityform =CommodityKeywordsRelateForm(request.POST)
        u_form = PartnersWebsiteUrlFormSet()
    
    return render_to_response('partners/website_create.html', {'form': form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform},
        context_instance=RequestContext(request))

        

@login_required
@permission_required('ippc.change_partnerswebsite', login_url="/accounts/login/")
def partner_websites_edit(request, partner, id=None, template_name='partners/website_edit.html'):
    """ Edit  website """
    user = request.user
    author = user
    partner = user.get_profile().partner
    # country_id = PestReport.objects.filter(country__country_id=country.id)
    user_partner_slug = lower(slugify(partner))
    if id:
        website = get_object_or_404(PartnersWebsite, partners=partner, pk=id)
    else:
        website = PartnersWebsite(author=request.user)
      
    if request.POST:
        form = PartnersWebsiteForm(request.POST,  request.FILES, instance=website)
        if website.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=website.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm(request.POST,instance=issues)
        else:
            issueform =IssueKeywordsRelateForm(request.POST)
        if website.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=website.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm(request.POST,instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm(request.POST)
        
        u_form = PartnersWebsiteUrlFormSet(request.POST,  instance=website)
        
        if form.is_valid()  and u_form.is_valid():
            form.save()
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = website
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = website
            commodity_instance.save()
            commodityform.save_m2m() 
    
           
            u_form.instance = website
            u_form.save()
            info(request, _("Successfully updated Website."))
            return redirect("partner-websites-detail", partners=user_partner_slug, year=website.publish_date.strftime("%Y"), month=website.publish_date.strftime("%m"), slug=website.slug)

    else:
        form = PartnersWebsiteForm(instance=website)
        if website.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=website.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm( instance=issues)
        else:
            issueform =IssueKeywordsRelateForm( )
        if website.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=website.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm( instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm()
        u_form =PartnersWebsiteUrlFormSet( instance=website)
      
    return render_to_response(template_name, {
        'form': form, 'u_form': u_form,'issueform': issueform,  'commodityform': commodityform, "website": website
    }, context_instance=RequestContext(request))
    








            
class CnPublicationListView(ListView):
    """   Contry Publication """
    context_object_name = 'latest'
    model = CnPublication
    date_field = 'publish_date'
    template_name = 'countries/cnpublication_list.html'
    queryset = CnPublication.objects.all().order_by('-publish_date', 'title')
    
    allow_future = False
    allow_empty = True
    paginate_by = 30

    def get_queryset(self):
        """ only return pest reports from the specific country """
        # self.country = get_object_or_404(CountryPage, country=self.kwargs['country'])
        self.country = self.kwargs['country']
        # CountryPage country_slug == country URL parameter keyword argument
        return CnPublication.objects.filter(country__country_slug=self.country)
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(CnPublicationListView, self).get_context_data(**kwargs)
        context['country'] = self.kwargs['country']
        return context
   
       
   
class CnPublicationDetailView(DetailView):
    """ Country Publication detail page """
    model = CnPublication
    context_object_name = 'cnpublication'
    template_name = 'countries/cnpublication_detail.html'
    queryset = CnPublication.objects.filter()



@login_required
@permission_required('ippc.add_cnpublication', login_url="/accounts/login/")
def country_publication_create(request, country):
    """ Create  Country Publication """
    user = request.user
    author = user
    country=user.get_profile().country
    user_country_slug = lower(slugify(country))

    form = CnPublicationForm(request.POST or None, request.FILES)
    issueform =IssueKeywordsRelateForm(request.POST)
    commodityform =CommodityKeywordsRelateForm(request.POST)
    
         
    if request.method == "POST":
        f_form = CnPublicationFileFormSet(request.POST, request.FILES)
        u_form = CnPublicationUrlFormSet(request.POST)
        if form.is_valid() and f_form.is_valid() and u_form.is_valid():
            new_cnpublication = form.save(commit=False)
            new_cnpublication.author = request.user
            new_cnpublication.author_id = author.id
            form.save()
            
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = new_cnpublication
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = new_cnpublication
            commodity_instance.save()
            commodityform.save_m2m()      
              
            f_form.instance = new_cnpublication
            f_form.save()
            u_form.instance = new_cnpublication
            u_form.save()
            info(request, _("Successfully added publication."))
            return redirect("country-publication-detail", country=user_country_slug, year=new_cnpublication.publish_date.strftime("%Y"), month=new_cnpublication.publish_date.strftime("%m"), slug=new_cnpublication.slug)
        else:
            return render_to_response('countries/cnpublication_create.html', {'form': form,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform},#'entryform': entryform,'docform':myformset,
             context_instance=RequestContext(request))

          
        
    else:
        form = CnPublicationForm(initial={'country': country}, instance=CnPublication())
        issueform =IssueKeywordsRelateForm(request.POST)
        commodityform =CommodityKeywordsRelateForm(request.POST)
        f_form = CnPublicationFileFormSet()
        u_form = CnPublicationUrlFormSet()
    
    return render_to_response('countries/cnpublication_create.html', {'form': form,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform},
        context_instance=RequestContext(request))

        

@login_required
@permission_required('ippc.change_cnpublication', login_url="/accounts/login/")
def country_publication_edit(request, country, id=None, template_name='countries/cnpublication_edit.html'):
    """ Edit   Country Publication """
    user = request.user
    author = user
    country = user.get_profile().country
    # country_id = PestReport.objects.filter(country__country_id=country.id)
    user_country_slug = lower(slugify(country))
    if id:
        cnpublication = get_object_or_404(CnPublication, country=country, pk=id)
    else:
        cnpublication = CnPublication(author=request.user)
      
    if request.POST:
        form = CnPublicationForm(request.POST,  request.FILES, instance=cnpublication)
        if cnpublication.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=cnpublication.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm(request.POST,instance=issues)
        else:
            issueform =IssueKeywordsRelateForm(request.POST)
        if cnpublication.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=cnpublication.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm(request.POST,instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm(request.POST)
        
        f_form = CnPublicationFileFormSet(request.POST,  request.FILES,instance=cnpublication)
        u_form = CnPublicationUrlFormSet(request.POST,  instance=cnpublication)
      
        if form.is_valid() and f_form.is_valid() and u_form.is_valid():
            form.save()
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = cnpublication
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = cnpublication
            commodity_instance.save()
            commodityform.save_m2m() 
    
            f_form.instance = cnpublication
            f_form.save()
            u_form.instance = cnpublication
            u_form.save()
            info(request, _("Successfully updated publication."))
            return redirect("country-publication-detail", country=user_country_slug, year=cnpublication.publish_date.strftime("%Y"), month=cnpublication.publish_date.strftime("%m"), slug=cnpublication.slug)

    else:
        form = CnPublicationForm(instance=cnpublication)
        if cnpublication.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=cnpublication.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm( instance=issues)
        else:
            issueform =IssueKeywordsRelateForm( )
        if cnpublication.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=cnpublication.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm( instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm()
        f_form = CnPublicationFileFormSet(instance=cnpublication)
        u_form = CnPublicationUrlFormSet( instance=cnpublication)
      
    return render_to_response(template_name, {
        'form': form, 'f_form':f_form,'u_form': u_form,'issueform': issueform,  'commodityform': commodityform, "cnpublication": cnpublication
    }, context_instance=RequestContext(request))            
            



class PartnersView(TemplateView):
    """ 
    Individual Partners homepage 
    """
    template_name = 'partners/partners_page.html'
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(TemplateView, self).get_context_data(**kwargs)
        context.update({
            'partner': self.kwargs['partner']
            # 'editors': self.kwargs['editors']
            # 'profile_user': self.kwargs['profile_user']
        })
        page = get_object_or_404(PartnersPage, name=self.kwargs['partner'])
        pageparent = get_object_or_404(PublicationLibrary, id=page.parent_id)
        titleparent=pageparent.title
        titleparent = titleparent.replace(" ", "-").lower()
        context['content']  =page.content
              
        context['titleparent']  =pageparent.title
        context['titleparentslug'] = titleparent
        #context['pageslug'] =  page.slug
        
        context['publications'] = PartnersPublication.objects.filter(partners__partner_slug=self.kwargs['partner'])
        context['news'] = PartnersNews.objects.filter(partners__partner_slug=self.kwargs['partner'])
        context['websites'] = PartnersWebsite.objects.filter(partners__partner_slug=self.kwargs['partner'])
       
        return context
    
     
    
       
   
class PartnersPublicationDetailView(DetailView):
    """ Partner Publication detail page """
    model = PartnersPublication
    context_object_name = 'partnerspublication'
    template_name = 'partners/p_publication_detail.html'
    queryset = PartnersPublication.objects.filter()
   
      
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(PartnersPublicationDetailView, self).get_context_data(**kwargs)
        page = get_object_or_404(PartnersPage, name=self.kwargs['partners'])
        context['pagetitle'] =  page.name
        context['pageslug'] =  page.slug
       # context['page'] =  page.partner_slug
        return context
     

            
@login_required
@permission_required('ippc.add_partnerspublication', login_url="/accounts/login/")
def partner_publication_create(request, partner):
    """ Create  partner Publication """
    user = request.user
    author = user
    partner=user.get_profile().partner
    user_partner_slug = lower(slugify(partner))

    form = PartnersPublicationForm(request.POST or None, request.FILES)
    issueform =IssueKeywordsRelateForm(request.POST)
    commodityform =CommodityKeywordsRelateForm(request.POST)
    
         
    if request.method == "POST":
        f_form = PartnersPublicationFileFormSet(request.POST, request.FILES)
        u_form = PartnersPublicationUrlFormSet(request.POST)
        if form.is_valid() and f_form.is_valid() and u_form.is_valid():
            new_partnerpublication = form.save(commit=False)
            new_partnerpublication.author = request.user
            new_partnerpublication.author_id = author.id
            form.save()
            
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = new_partnerpublication
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = new_partnerpublication
            commodity_instance.save()
            commodityform.save_m2m()      
              
            f_form.instance = new_partnerpublication
            f_form.save()
            u_form.instance = new_partnerpublication
            u_form.save()
            info(request, _("Successfully added publication."))
            return redirect("partner-publication-detail", partners=user_partner_slug, year=new_partnerpublication.publish_date.strftime("%Y"), month=new_partnerpublication.publish_date.strftime("%m"), slug=new_partnerpublication.slug)
        else:
            return render_to_response('partners/p_publication_create.html', {'form': form,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform},#'entryform': entryform,'docform':myformset,
             context_instance=RequestContext(request))

          
        
    else:
        form = PartnersPublicationForm(initial={'partner': partner}, instance=PartnersPublication())
        issueform =IssueKeywordsRelateForm(request.POST)
        commodityform =CommodityKeywordsRelateForm(request.POST)
        f_form = PartnersPublicationFileFormSet()
        u_form = PartnersPublicationUrlFormSet()
    
    return render_to_response('partners/p_publication_create.html', {'form': form,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform},
        context_instance=RequestContext(request))

        

@login_required
@permission_required('ippc.change_partnerspublication', login_url="/accounts/login/")
def partner_publication_edit(request, partner, id=None, template_name='partners/p_publication_edit.html'):
    """ Edit   partners Publication """
    user = request.user
    author = user
    partner = user.get_profile().partner
    # country_id = PestReport.objects.filter(country__country_id=country.id)
    user_partner_slug = lower(slugify(partner))
    if id:
        partnerspublication = get_object_or_404(PartnersPublication, partners=partner, pk=id)
    else:
        partnerspublication = PartnersPublication(author=request.user)
      
    if request.POST:
        form =PartnersPublicationForm(request.POST,  request.FILES, instance=partnerspublication)
        if partnerspublication.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=partnerspublication.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm(request.POST,instance=issues)
        else:
            issueform =IssueKeywordsRelateForm(request.POST)
        if partnerspublication.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=partnerspublication.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm(request.POST,instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm(request.POST) 
        f_form = PartnersPublicationFileFormSet(request.POST,  request.FILES,instance=partnerspublication)
        u_form = PartnersPublicationUrlFormSet(request.POST,  instance=partnerspublication)
      
        if form.is_valid() and f_form.is_valid() and u_form.is_valid():
            form.save()
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = partnerspublication
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = partnerspublication
            commodity_instance.save()
            commodityform.save_m2m() 
    
            f_form.instance = partnerspublication
            f_form.save()
            u_form.instance = partnerspublication
            u_form.save()
            info(request, _("Successfully updated publication."))
            return redirect("partner-publication-detail", partners=user_partner_slug, year=partnerspublication.publish_date.strftime("%Y"), month=partnerspublication.publish_date.strftime("%m"), slug=partnerspublication.slug)

    else:
        form = PartnersPublicationForm(instance=partnerspublication)
        if partnerspublication.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=partnerspublication.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm( instance=issues)
        else:
            issueform =IssueKeywordsRelateForm( )
        if partnerspublication.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=partnerspublication.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm( instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm()
        f_form = PartnersPublicationFileFormSet(instance=partnerspublication)
        u_form = PartnersPublicationUrlFormSet( instance=partnerspublication)
      
    return render_to_response(template_name, {
        'form': form, 'f_form':f_form,'u_form': u_form,'issueform': issueform,  'commodityform': commodityform, "partnerspublication": partnerspublication
    }, context_instance=RequestContext(request))            
                        
            
            
class PestFreeAreaListView(ListView):
    """    Event Reporting """
    context_object_name = 'latest'
    model = PestFreeArea
    date_field = 'publish_date'
    template_name = 'countries/pfa_list.html'
    queryset = PestFreeArea.objects.all().order_by('-publish_date', 'title')
    
    allow_future = False
    allow_empty = True
    paginate_by = 30

    def get_queryset(self):
        """ only return PestFreeArea from the specific country """
        # self.country = get_object_or_404(CountryPage, country=self.kwargs['country'])
        self.country = self.kwargs['country']
        # CountryPage country_slug == country URL parameter keyword argument
        return PestFreeArea.objects.filter(country__country_slug=self.country)
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(PestFreeAreaListView, self).get_context_data(**kwargs)
        context['country'] = self.kwargs['country']
        return context
   
       
   
class PestFreeAreaDetailView(DetailView):
    """ PestFreeArea Detail page """
    model = PestFreeArea
    context_object_name = 'pfa'
    template_name = 'countries/pfa_detail.html'
    queryset = PestFreeArea.objects.filter()



@login_required
@permission_required('ippc.add_pestfreearea', login_url="/accounts/login/")
def pfa_create(request, country):
    """ Create PestFreeArea """
    user = request.user
    author = user
    country=user.get_profile().country
    user_country_slug = lower(slugify(country))


    form = PestFreeAreaForm(request.POST)
    issueform =IssueKeywordsRelateForm(request.POST)
    commodityform =CommodityKeywordsRelateForm(request.POST)
    notifyrelateform =NotificationMessageRelateForm(request.POST)
     
    if request.method == "POST":
         f_form = PestFreeAreaFileFormSet(request.POST, request.FILES)
         u_form = PestFreeAreaUrlFormSet(request.POST)

         if form.is_valid() and f_form.is_valid() and u_form.is_valid():
            new_pfa = form.save(commit=False)
            new_pfa.author = request.user
            new_pfa.author_id = author.id
            form.save()
            
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = new_pfa
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = new_pfa
            commodity_instance.save()
            commodityform.save_m2m() 
            
            notify_instance = notifyrelateform.save(commit=False)
            notify_instance.content_object = new_pfa
            notify_instance.save()
            notifyrelateform.save_m2m()
            
            f_form.instance = new_pfa
            f_form.save()
            
            u_form.instance = new_pfa
            u_form.save()
            content_type = ContentType.objects.get_for_model(new_pfa)
            send_notification_message(1,new_pfa.id,content_type,new_pfa.title,user_country_slug+'/pestfreeareas/'+str(new_pfa.publish_date.strftime("%Y"))+'/'+str(new_pfa.publish_date.strftime("%m"))+'/'+new_pfa.slug+'/')
           
            info(request, _("Successfully created PestFreeArea."))
            
            return redirect("pfa-detail", country=user_country_slug, year=new_pfa.publish_date.strftime("%Y"), month=new_pfa.publish_date.strftime("%m"), slug=new_pfa.slug)
         else:
             return render_to_response('countries/pfa_create.html', {'form': form,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform,'notifyrelateform':notifyrelateform},
             context_instance=RequestContext(request))
    else:
        form = PestFreeAreaForm(initial={'country': country}, instance=PestFreeArea())
        issueform =IssueKeywordsRelateForm(request.POST)
        commodityform =CommodityKeywordsRelateForm(request.POST)
        notifyrelateform =NotificationMessageRelateForm(request.POST)
        f_form =PestFreeAreaFileFormSet()
        u_form = PestFreeAreaUrlFormSet()

    return render_to_response('countries/pfa_create.html', {'form': form  ,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform,'notifyrelateform':notifyrelateform},
        context_instance=RequestContext(request))


        
# http://stackoverflow.com/a/1854453/412329
@login_required
@permission_required('ippc.change_pestfreearea', login_url="/accounts/login/")
def pfa_edit(request, country, id=None, template_name='countries/pfa_edit.html'):
    """ Edit PestFreeArea """
    user = request.user
    author = user
    country = user.get_profile().country
    # country_id = PestReport.objects.filter(country__country_id=country.id)
    user_country_slug = lower(slugify(country))
    if id:
        pfa = get_object_or_404(PestFreeArea, country=country, pk=id)
        content_type = ContentType.objects.get_for_model(pfa)
        try:
            notifications = get_object_or_404(NotificationMessageRelate, object_id=id,content_type__pk=content_type.id)
        except:
            notifications = None
        # if pest_report.author != request.user:
        #     return HttpResponseForbidden()
    else:
        pfa = PestFreeArea(author=request.user)
      
    if request.POST:

        form = PestFreeAreaForm(request.POST,  request.FILES, instance=pfa)
        if pfa.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=pfa.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm(request.POST,instance=issues)
        else:
            issueform =IssueKeywordsRelateForm(request.POST)
        if pfa.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=pfa.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm(request.POST,instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm(request.POST)
        notifyrelateform =NotificationMessageRelateForm(request.POST,instance=notifications)
        f_form = PestFreeAreaFileFormSet(request.POST,  request.FILES,instance=pfa)
        u_form = PestFreeAreaUrlFormSet(request.POST,  instance=pfa)
        if form.is_valid() and f_form.is_valid() and u_form.is_valid():
            form.save()
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = pfa
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = pfa
            commodity_instance.save()
            commodityform.save_m2m() 
            
            notify_instance = notifyrelateform.save(commit=False)
            notify_instance.content_object = pfa
            notify_instance.save()
            notifyrelateform.save_m2m()
            
            f_form.instance = pfa
            f_form.save()
            u_form.instance = pfa
            u_form.save()
            
            send_notification_message(0,id,content_type,pfa.title,user_country_slug+'/pestfreeareas/'+str(pfa.publish_date.strftime("%Y"))+'/'+str(pfa.publish_date.strftime("%m"))+'/'+pfa.slug+'/')
            # If the save was successful, success message and redirect to another page
            # info(request, _("Successfully updated pest report."))
            return redirect("pfa-detail", country=user_country_slug, year=pfa.publish_date.strftime("%Y"), month=pfa.publish_date.strftime("%m"), slug=pfa.slug)

    else:
        form = PestFreeAreaForm(instance=pfa)
        if pfa.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=pfa.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm( instance=issues)
        else:
            issueform =IssueKeywordsRelateForm( )
        if pfa.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=pfa.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm( instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm()
        notifyrelateform =NotificationMessageRelateForm(instance=notifications)
        f_form = PestFreeAreaFileFormSet(instance=pfa)
        u_form = PestFreeAreaUrlFormSet(instance=pfa)
        
    return render_to_response(template_name, {
        'form': form,'f_form':f_form,'u_form':u_form,'issueform': issueform,'commodityform': commodityform,  "pfa": pfa,'notifyrelateform':notifyrelateform
    }, context_instance=RequestContext(request))
    

class ImplementationISPMListView(ListView):
    """    ImplementationISPM """
    context_object_name = 'latest'
    model = ImplementationISPM
    date_field = 'publish_date'
    template_name = 'countries/implementationispm_list.html'
    queryset = ImplementationISPM.objects.all().order_by('-publish_date', 'title')
    
    allow_future = False
    allow_empty = True
    paginate_by = 30

    def get_queryset(self):
        """ only return pest reports from the specific country """
        # self.country = get_object_or_404(CountryPage, country=self.kwargs['country'])
        self.country = self.kwargs['country']
        # CountryPage country_slug == country URL parameter keyword argument
        return ImplementationISPM.objects.filter(country__country_slug=self.country)
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(ImplementationISPMListView, self).get_context_data(**kwargs)
        context['country'] = self.kwargs['country']
        return context
   
       
   
class ImplementationISPMDetailView(DetailView):
    """ ImplementationISPM detail page """
    model = ImplementationISPM
    context_object_name = 'implementationispm'
    template_name = 'countries/implementationispm_detail.html'
    queryset = ImplementationISPM.objects.filter()



@login_required
@permission_required('ippc.add_implementationispm', login_url="/accounts/login/")
def implementationispm_create(request, country):
    """ Create ImplementationISPM """
    user = request.user
    author = user
    country=user.get_profile().country
    user_country_slug = lower(slugify(country))


    form = ImplementationISPMForm(request.POST)
    issueform =IssueKeywordsRelateForm(request.POST)
    commodityform =CommodityKeywordsRelateForm(request.POST)
    notifyrelateform =NotificationMessageRelateForm(request.POST)
     
    if request.method == "POST":
        f_form =ImplementationISPMFileFormSet(request.POST, request.FILES)
        u_form =ImplementationISPMUrlFormSet(request.POST)
        if form.is_valid() and f_form.is_valid() and u_form.is_valid():
            new_implementationispm = form.save(commit=False)
            new_implementationispm.author = request.user
            new_implementationispm.author_id = author.id
            form.save()
            
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = new_implementationispm
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = new_implementationispm
            commodity_instance.save()
            commodityform.save_m2m()
            
            notify_instance = notifyrelateform.save(commit=False)
            notify_instance.content_object = new_implementationispm
            notify_instance.save()
            notifyrelateform.save_m2m()
            
            f_form.instance = new_implementationispm
            f_form.save()
            u_form.instance = new_implementationispm
            u_form.save()
            content_type = ContentType.objects.get_for_model(new_implementationispm)
            send_notification_message(1,new_implementationispm.id,content_type,new_implementationispm.title,user_country_slug+'/implementationispm/'+str(new_implementationispm.publish_date.strftime("%Y"))+'/'+str(new_implementationispm.publish_date.strftime("%m"))+'/'+new_implementationispm.slug+'/')
            info(request, _("Successfully created implementationispm."))
            
            return redirect("implementationispm-detail", country=user_country_slug, year=new_implementationispm.publish_date.strftime("%Y"), month=new_implementationispm.publish_date.strftime("%m"), slug=new_implementationispm.slug)
        else:
             return render_to_response('countries/implementationispm_create.html', {'form': form,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform,'notifyrelateform':notifyrelateform},
             context_instance=RequestContext(request))
    else:
        form = ImplementationISPMForm(initial={'country': country}, instance=ImplementationISPM())
        issueform =IssueKeywordsRelateForm(request.POST)
        commodityform =CommodityKeywordsRelateForm(request.POST)
        notifyrelateform =NotificationMessageRelateForm(request.POST)
        f_form =ImplementationISPMFileFormSet()
        u_form =ImplementationISPMUrlFormSet()

    return render_to_response('countries/implementationispm_create.html', {'form': form  ,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform,'notifyrelateform':notifyrelateform},
        context_instance=RequestContext(request))


        
# http://stackoverflow.com/a/1854453/412329
@login_required
@permission_required('ippc.change_implementationispm', login_url="/accounts/login/")
def implementationispm_edit(request, country, id=None, template_name='countries/implementationispm_edit.html'):
    """ Edit implementationispm """
    user = request.user
    author = user
    country = user.get_profile().country
    # country_id = PestReport.objects.filter(country__country_id=country.id)
    user_country_slug = lower(slugify(country))
    if id:
        implementationispm = get_object_or_404(ImplementationISPM, country=country, pk=id)
        content_type = ContentType.objects.get_for_model(implementationispm)
        try:
            notifications = get_object_or_404(NotificationMessageRelate, object_id=id,content_type__pk=content_type.id)
        except:
            notifications = None
       # if pest_report.author != request.user:
        #     return HttpResponseForbidden()
    else:
        implementationispm = ImplementationISPM(author=request.user)
      
    if request.POST:
        form = ImplementationISPMForm(request.POST,  request.FILES, instance=implementationispm)
        if implementationispm.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=implementationispm.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm(request.POST,instance=issues)
        else:
            issueform =IssueKeywordsRelateForm(request.POST)
        if implementationispm.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=implementationispm.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm(request.POST,instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm(request.POST)
        
        notifyrelateform =NotificationMessageRelateForm(request.POST,instance=notifications)
        f_form = ImplementationISPMFileFormSet(request.POST,  request.FILES,instance=implementationispm)
        u_form = ImplementationISPMUrlFormSet(request.POST,  instance=implementationispm)
        if form.is_valid() and f_form.is_valid() and u_form.is_valid():
            form.save()
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = implementationispm
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = implementationispm
            commodity_instance.save()
            commodityform.save_m2m() 
            
            notify_instance = notifyrelateform.save(commit=False)
            notify_instance.content_object = implementationispm
            notify_instance.save()
            notifyrelateform.save_m2m()
            
            f_form.instance = implementationispm
            f_form.save()
            u_form.instance = implementationispm
            u_form.save()
            send_notification_message(0,id,content_type,implementationispm.title,user_country_slug+'/implementationispm/'+str(implementationispm.publish_date.strftime("%Y"))+'/'+str(implementationispm.publish_date.strftime("%m"))+'/'+implementationispm.slug+'/')
            
            # If the save was successful, success message and redirect to another page
            # info(request, _("Successfully updated pest report."))
            return redirect("implementationispm-detail", country=user_country_slug, year=implementationispm.publish_date.strftime("%Y"), month=implementationispm.publish_date.strftime("%m"), slug=implementationispm.slug)

    else:
        form = ImplementationISPMForm(instance=implementationispm)
        if implementationispm.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=implementationispm.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm( instance=issues)
        else:
            issueform =IssueKeywordsRelateForm( )
        if implementationispm.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=implementationispm.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm( instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm()
        notifyrelateform =NotificationMessageRelateForm(instance=notifications)
        f_form = ImplementationISPMFileFormSet(instance=implementationispm)
        u_form = ImplementationISPMUrlFormSet(instance=implementationispm)
    return render_to_response(template_name, {
        'form': form,'f_form':f_form,'u_form': u_form,'issueform': issueform,'commodityform': commodityform,  "implementationispm": implementationispm,'notifyrelateform':notifyrelateform
    }, context_instance=RequestContext(request))

    #/**************************************************************/
class CountryNewsListView(ListView):
    """    CountryNews """
    context_object_name = 'latest'
    model = CountryNews
    date_field = 'publish_date'
    template_name = 'countries/countrynews_list.html'
    queryset = CountryNews.objects.all().order_by('-publish_date', 'title')
    
    allow_future = False
    allow_empty = True
    paginate_by = 30

    def get_queryset(self):
        """ only return CountryNews from the specific country """
        # self.country = get_object_or_404(CountryPage, country=self.kwargs['country'])
        self.country = self.kwargs['country']
        # CountryPage country_slug == country URL parameter keyword argument
        return CountryNews.objects.filter(country__country_slug=self.country)
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(CountryNewsListView, self).get_context_data(**kwargs)
        context['country'] = self.kwargs['country']
        return context
   
       
   
class CountryNewsDetailView(DetailView):
    """ CountryNews detail page """
    model = CountryNews
    context_object_name = 'countrynews'
    template_name = 'countries/countrynews_detail.html'
    queryset = CountryNews.objects.filter()



@login_required
@permission_required('ippc.add_countrynews', login_url="/accounts/login/")
def countrynews_create(request, country):
    """ Create countrynews """
    user = request.user
    author = user
    country=user.get_profile().country
    user_country_slug = lower(slugify(country))


    form = CountryNewsForm(request.POST)
    issueform =IssueKeywordsRelateForm(request.POST)
    commodityform =CommodityKeywordsRelateForm(request.POST)
    
    if request.method == "POST":
        f_form =CountryNewsFileFormSet(request.POST, request.FILES)
        u_form =CountryNewsUrlFormSet(request.POST)
        if form.is_valid() and f_form.is_valid() and u_form.is_valid():
            new_countrynews = form.save(commit=False)
            new_countrynews.author = request.user
            new_countrynews.author_id = author.id
            form.save()
            
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = new_countrynews
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = new_countrynews
            commodity_instance.save()
            commodityform.save_m2m()
            
            f_form.instance = new_countrynews
            f_form.save()
            u_form.instance = new_countrynews
            u_form.save()
            
            info(request, _("Successfully created news."))
            
            return redirect("country-news-detail", country=user_country_slug, year=new_countrynews.publish_date.strftime("%Y"), month=new_countrynews.publish_date.strftime("%m"), slug=new_countrynews.slug)
        else:
             return render_to_response('countries/countrynews_create.html', {'form': form,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform},
             context_instance=RequestContext(request))
    else:
        form = CountryNewsForm(initial={'country': country}, instance=CountryNews())
        issueform =IssueKeywordsRelateForm(request.POST)
        commodityform =CommodityKeywordsRelateForm(request.POST)
        f_form =CountryNewsFileFormSet()
        u_form =CountryNewsUrlFormSet()

    return render_to_response('countries/countrynews_create.html', {'form': form  ,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform},
        context_instance=RequestContext(request))


        
# http://stackoverflow.com/a/1854453/412329
@login_required
@permission_required('ippc.change_countrynews', login_url="/accounts/login/")
def countrynews_edit(request, country, id=None, template_name='countries/countrynews_edit.html'):
    """ Edit countrynews """
    user = request.user
    author = user
    country = user.get_profile().country
    # country_id = PestReport.objects.filter(country__country_id=country.id)
    user_country_slug = lower(slugify(country))
    if id:
        countrynews = get_object_or_404(CountryNews, country=country, pk=id)
       # if pest_report.author != request.user:
        #     return HttpResponseForbidden()
    else:
        countrynews = CountryNews(author=request.user)
      
    if request.POST:
        form = CountryNewsForm(request.POST,  request.FILES, instance=countrynews)
        if countrynews.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=countrynews.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm(request.POST,instance=issues)
        else:
            issueform =IssueKeywordsRelateForm(request.POST)
        if cnpublication.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=countrynews.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm(request.POST,instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm(request.POST)
        f_form = CountryNewsFileFormSet(request.POST,  request.FILES,instance=countrynews)
        u_form = CountryNewsUrlFormSet(request.POST,  instance=countrynews)
        if form.is_valid() and f_form.is_valid() and u_form.is_valid():
            form.save()
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = countrynews
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = countrynews
            commodity_instance.save()
            commodityform.save_m2m() 
            
            f_form.instance = countrynews
            f_form.save()
            u_form.instance = countrynews
            u_form.save()
            # If the save was successful, success message and redirect to another page
            # info(request, _("Successfully updated pest report."))
            return redirect("country-news-detail", country=user_country_slug, year=countrynews.publish_date.strftime("%Y"), month=countrynews.publish_date.strftime("%m"), slug=countrynews.slug)

    else:
        form = CountryNewsForm(instance=countrynews)
        if countrynews.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=countrynews.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm(instance=issues)
        else:
            issueform =IssueKeywordsRelateForm( )
        if cnpublication.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=countrynews.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm( instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm( )
      
        f_form = CountryNewsFileFormSet(instance=countrynews)
        u_form = CountryNewsUrlFormSet(instance=countrynews)
    return render_to_response(template_name, {
        'form': form,'f_form':f_form,'u_form': u_form,'issueform': issueform,'commodityform': commodityform,  "countrynews": countrynews
    }, context_instance=RequestContext(request))
   
   
   
   
   
   
   
   
class PartnersNewsDetailView(DetailView):
    """ Partners News detail page """
    model = PartnersNews
    context_object_name = 'partnersnews'
    template_name = 'partners/partnersnews_detail.html'
    queryset = PartnersNews.objects.filter()
      
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(PartnersNewsDetailView, self).get_context_data(**kwargs)
        page = get_object_or_404(PartnersPage, name=self.kwargs['partners'])
        context['pagetitle'] =  page.name
        context['pageslug'] =  page.slug
       # context['page'] =  page.partner_slug
        return context
     


@login_required
@permission_required('ippc.add_partnersnews', login_url="/accounts/login/")
def partners_news_create(request, partner):
    """ Create partnersnews """
    user = request.user
    author = user
    partner=user.get_profile().partner
    user_partner_slug = lower(slugify(partner))


    form = PartnersNewsForm(request.POST)
    issueform =IssueKeywordsRelateForm(request.POST)
    commodityform =CommodityKeywordsRelateForm(request.POST)
    
    if request.method == "POST":
        f_form =PartnersNewsFileFormSet(request.POST, request.FILES)
        u_form =PartnersNewsUrlFormSet(request.POST)
        if form.is_valid() and f_form.is_valid() and u_form.is_valid():
            new_partnersnews = form.save(commit=False)
            new_partnersnews.author = request.user
            new_partnersnews.author_id = author.id
            form.save()
            
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = new_partnersnews
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = new_partnersnews
            commodity_instance.save()
            commodityform.save_m2m()
            
            f_form.instance = new_partnersnews
            f_form.save()
            u_form.instance = new_partnersnews
            u_form.save()
            
            info(request, _("Successfully created news."))
            
            return redirect("partner-news-detail", partners=user_partner_slug, year=new_partnersnews.publish_date.strftime("%Y"), month=new_partnersnews.publish_date.strftime("%m"), slug=new_partnersnews.slug)
        else:
             return render_to_response('partners/partnersnews_create.html', {'form': form,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform},
             context_instance=RequestContext(request))
    else:
        form = PartnersNewsForm(initial={'partners': partner}, instance=PartnersNews())
        issueform =IssueKeywordsRelateForm(request.POST)
        commodityform =CommodityKeywordsRelateForm(request.POST)
        f_form = PartnersNewsFileFormSet()
        u_form = PartnersNewsUrlFormSet()

    return render_to_response('partners/partnersnews_create.html', {'form': form  ,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform},
        context_instance=RequestContext(request))


        
# http://stackoverflow.com/a/1854453/412329
@login_required
@permission_required('ippc.change_partnersnews', login_url="/accounts/login/")
def partners_news_edit(request, partner, id=None, template_name='partners/partnersnews_edit.html'):
    """ Edit partner news """
    user = request.user
    author = user
    partner = user.get_profile().partner
    # country_id = PestReport.objects.filter(country__country_id=country.id)
    user_partner_slug = lower(slugify(partner))
    if id:
        partnernews = get_object_or_404( PartnersNews,  partners= partner, pk=id)
    else:
        partnernews =  PartnersNews(author=request.user)
      
    if request.POST:
        form =  PartnersNewsForm(request.POST,  request.FILES, instance=partnernews)
        if partnernews.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=partnernews.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm(request.POST,instance=issues)
        else:
            issueform =IssueKeywordsRelateForm(request.POST)
        if partnernews.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=partnernews.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm(request.POST,instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm(request.POST)
        f_form =  PartnersNewsFileFormSet(request.POST,  request.FILES,instance=partnernews)
        u_form =  PartnersNewsUrlFormSet(request.POST,  instance=partnernews)
        if form.is_valid() and f_form.is_valid() and u_form.is_valid():
            form.save()
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = partnernews
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = partnernews
            commodity_instance.save()
            commodityform.save_m2m() 
            
            f_form.instance = partnernews
            f_form.save()
            u_form.instance = partnernews
            u_form.save()
            # If the save was successful, success message and redirect to another page
            # info(request, _("Successfully updated pest report."))
            return redirect("partner-news-detail", partners=user_partner_slug, year=partnernews.publish_date.strftime("%Y"), month=partnernews.publish_date.strftime("%m"), slug=partnernews.slug)

    else:
        form = PartnersNewsForm(instance=partnernews)
        if partnernews.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=partnernews.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm( instance=issues)
        else:
            issueform =IssueKeywordsRelateForm( )
        if partnernews.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=partnernews.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm( instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm()
        f_form = PartnersNewsFileFormSet(instance=partnernews)
        u_form = PartnersNewsUrlFormSet(instance=partnernews)
    return render_to_response(template_name, {
        'form': form,'f_form':f_form,'u_form': u_form,'issueform': issueform,'commodityform': commodityform,  "partnernews": partnernews
    }, context_instance=RequestContext(request))
   
    
   
   
   
@login_required
@permission_required('ippc.change_publication', login_url="/accounts/login/")
def publication_edit(request, id=None, template_name='pages/publication_edit.html'):
    """ Edit  Publication """
    user = request.user
    author = user
    if id:
        publication = get_object_or_404(Publication, pk=id)
        
    #    if publication.issuename:
    #        print(publication.issuename.all[0])
    #    issues = get_object_or_404(IssueKeywordsRelate, pk=publication.issuename.all()[0].id)
    #    commodities = get_object_or_404(CommodityKeywordsRelate, pk=publication.commname.all()[0].id)
    else:
        publication = Publication(author=request.user)
      
    if request.POST:
        form = PublicationForm(request.POST,  request.FILES, instance=publication)
        if publication.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=publication.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm(request.POST,instance=issues)
        else:
            issueform =IssueKeywordsRelateForm(request.POST)
        if publication.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=publication.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm(request.POST,instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm(request.POST)
        f_form = PublicationFileFormSet(request.POST,  request.FILES,instance=publication)
        u_form = PublicationUrlFormSet(request.POST,  instance=publication)
      
        if form.is_valid() and f_form.is_valid() and u_form.is_valid():
            form.save()
            issue_instance = issueform.save(commit=False)
            issue_instance.content_object = publication
            issue_instance.save()
            issueform.save_m2m()
            
            commodity_instance = commodityform.save(commit=False)
            commodity_instance.content_object = publication
            commodity_instance.save()
            commodityform.save_m2m() 
    
            f_form.instance = publication
            f_form.save()
            u_form.instance = publication
            u_form.save()
            info(request, _("Successfully updated publication."))
            return redirect("publication-detail", pk=publication.id)

    else:
        form = PublicationForm(instance=publication)
        
        if publication.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=publication.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm( instance=issues)
        else:
            issueform =IssueKeywordsRelateForm( )
        if publication.commname.count()>0:
            commodities = get_object_or_404(CommodityKeywordsRelate, pk=publication.commname.all()[0].id)
            commodityform =CommodityKeywordsRelateForm( instance=commodities)
        else:
            commodityform =CommodityKeywordsRelateForm()
        f_form = PublicationFileFormSet(instance=publication)
        u_form = PublicationUrlFormSet( instance=publication)
      
    return render_to_response(template_name, {
        'form': form, 'f_form':f_form,'u_form': u_form,'issueform': issueform,  'commodityform': commodityform, "publication": publication
    }, context_instance=RequestContext(request))       
    
    
class CountryListView(ListView):
    """   alphabetic countries list  """
    context_object_name = 'latest'
    model = CountryPage
    template_name = 'countries/countries_list.html'
    queryset = CountryPage.objects.all().order_by('title')
    #region_name=self.kwargs['region']
   
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(CountryListView, self).get_context_data(**kwargs)
        context['number_of_cp']= CountryPage.objects.filter(cp_ncp_t_type='CP').count()
        if self.kwargs['region'] == 'all':
            context['countries']= CountryPage.objects.all()
        else:
            for k,v in REGIONS:
                reg = v.lower()
                reg = reg.replace(" ", "-");
                if reg == self.kwargs['region']:
                    kindex=k
                    context['region_name']=v
            context['countries']= CountryPage.objects.filter(region=kindex)
        return context

    
class CountryStatsTotalreportsListView(ListView):
    """   Statistics reports  """
    context_object_name = 'latest'
    model = CountryPage
    template_name = 'countries/countries_statstotalreports.html'
    queryset = CountryPage.objects.all().order_by('title')
   
    def get_context_data(self, **kwargs): 
        context = super(CountryStatsTotalreportsListView, self).get_context_data(**kwargs)
        context['dategenerate']=timezone.now()
        datachart1=''
        datachart2=''
        datachart3=''
        tot_rep_count=0
        tot_ev_count1=0
        tot_ev_count2=0
        results_list = []
        tot = []
        p_count=PestReport.objects.filter().count()
        tot.append(p_count)
        tot_ev_count1+=p_count
        for i in range(1,6):
           rep_count=ReportingObligation.objects.filter(reporting_obligation_type=i).count()
           tot_rep_count+=rep_count
           ev_count=EventReporting.objects.filter(event_rep_type=i).count()
           if i<=2:
               tot_ev_count1+=ev_count
           else:    
               tot_ev_count2+=ev_count
           tot.append(rep_count)
           tot.append(ev_count)
        results_list.append(tot)
        context['results_list']=results_list
        
        for r in results_list:
             datachart1 += ' {  y: '+str(r[1]*100/tot_rep_count)+', legendText:"Description of the NPPO", label: "Description of the NPPO: '+str(r[1]*100/tot_rep_count)+'%" },'
             datachart1 += ' {  y: '+str(r[3]*100/tot_rep_count)+', legendText:"Entry points", label: "Entry points: '+str(r[3]*100/tot_rep_count)+'%" },'
             datachart1 += ' {  y: '+str(r[5]*100/tot_rep_count)+', legendText:"List of regulated pests", label: "List of regulated pests: '+str(r[5]*100/tot_rep_count)+'%" },'
             datachart1 += ' {  y: '+str(r[7]*100/tot_rep_count)+', legendText:"Phytosanitary restrictions", label: "Phytosanitary restrictions: '+str(r[7]*100/tot_rep_count)+'%" },'
	
             datachart2 += ' {  y: '+str(r[4]*100/tot_ev_count1)+', legendText:"Non compliance", label: "Non compliance: '+str(r[4]*100/tot_rep_count)+'%" },'
             datachart2 += ' {  y: '+str(r[2]*100/tot_ev_count1)+', legendText:"Emergency actions", label: "Emergency actions: '+str(r[2]*100/tot_rep_count)+'%" },'
             datachart2 += ' {  y: '+str(r[0]*100/tot_ev_count1)+', legendText:"Pest report", label: "Pest report: '+str(r[0]*100/tot_rep_count)+'%" },'
            
             if r[6]>0:
                datachart3 += ' {  y: '+str(r[6]*100/tot_ev_count2)+', legendText:"Organizational (NPPO info)", label: "Organizational (NPPO info): '+str(r[6]*100/tot_rep_count)+'%" },'
             if r[10]>0:
                datachart3 += ' {  y: '+str(r[10]*100/tot_ev_count2)+', legendText:"PRA (rationale phytosanitary requirements) ", label: "PRA (rationale phytosanitary requirements): '+str(r[10]*100/tot_rep_count)+'%" },'
             if r[8]>0:
                datachart3 += ' {  y: '+str(r[8]*100/tot_ev_count2)+', legendText:"Pest status", label: "Pest status: '+str(r[8]*100/tot_rep_count)+'%" },'
        context['datachart1']=datachart1
        context['datachart2']=datachart2
        context['datachart3']=datachart3
        return context   
	

class CountryStatsreportsListView(ListView):
    """   Statistics reports  """
    context_object_name = 'latest'
    model = CountryPage
    template_name = 'countries/countries_statsreports.html'
    queryset = CountryPage.objects.all().order_by('title')
   
    def get_context_data(self, **kwargs): 
        context = super(CountryStatsreportsListView, self).get_context_data(**kwargs)
        context['dategenerate']=timezone.now()
        results_list = []
        countriesList=CountryPage.objects.filter().exclude(id='-1')
        for c in countriesList:
             totcn = []
             totcn.append(c)    
             p_count=PestReport.objects.filter(country_id=c.id).count()
             totcn.append(p_count)
             for i in range(1,6):
                rep_count=ReportingObligation.objects.filter(country_id=c.id,reporting_obligation_type=i).count()
                ev_count=EventReporting.objects.filter(country_id=c.id,event_rep_type=i).count()
                totcn.append(rep_count)
                totcn.append(ev_count)
             totcn.append((slugify(c)))
             results_list.append(totcn)
        context['results_list']=results_list
    
        return context
  
class CountryRegionsPercentageListView(ListView):
    """   stat  """
    context_object_name = 'latest'
    model = CountryPage
    template_name = 'countries/countries_regionspercentage.html'
    queryset = CountryPage.objects.all().order_by('title')
   
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(CountryRegionsPercentageListView, self).get_context_data(**kwargs)
        context['dategenerate']=timezone.now()
        regionCN = []
        regionCNcp = []
        regionCNncp = []
        
        regionpest = []
        regionrep1 = []
        regionrep2 = []
        regionrep3 = []
        regionrep4 = []
        regionev1 = []
        regionev2 = []
        regionev3 = []
        regionev4 = []
        regionev5 = []
        regionpestcp = []
        regionrep1cp = []
        regionrep2cp = []
        regionrep3cp= []
        regionrep4cp = []
        regionev1cp = []
        regionev2cp = []
        regionev3cp = []
        regionev4cp = []
        regionev5cp = []
        regionpestncp = []
        regionrep1ncp= []
        regionrep2ncp = []
        regionrep3ncp = []
        regionrep4ncp = []
        regionev1ncp = []
        regionev2ncp = []
        regionev3ncp = []
        regionev4ncp = []
        regionev5ncp = []
        for k,v in REGIONS:
                reg = v.lower()
                numCN = []
                countriesperregion=CountryPage.objects.filter(region=k).exclude(cp_ncp_t_type='T')
                numb_countriesperregion=countriesperregion.count()
                numCN.append(reg)
                numCN.append(numb_countriesperregion)
                regionCN.append(numCN)
                context['region_cn']=regionCN
                
                numCNcp = []
                countriesperregioncp=CountryPage.objects.filter(region=k,cp_ncp_t_type='CP')
                numb_countriesperregioncp=countriesperregioncp.count()
                numCNcp.append(reg)
                numCNcp.append(numb_countriesperregioncp)
                regionCNcp.append(numCNcp)
                context['region_cp']=regionCNcp
                
                numCNncp = []
                countriesperregionncp=CountryPage.objects.filter(region=k,cp_ncp_t_type='NCP')
                numb_countriesperregionncp=countriesperregionncp.count()
                numCNncp.append(reg)
                numCNncp.append(numb_countriesperregionncp)
                regionCNncp.append(numCNncp)
                context['region_ncp']=regionCNncp
                
                pests = []
                p_count=0
                for c in countriesperregion:
                    p=PestReport.objects.filter(country_id=c.id)
                    p_count+=p.count()
                pestC=(int)((p_count * 100)/numb_countriesperregion)
                pests.append(pestC)
                regionpest.append(pests)   
                context['region_pest']=regionpest
                
                for i in range(1,6):
                    rep_count=0
                    ev_count=0
                    reporting_array = []
                    evreporting_array=[]
                    for c in countriesperregion:
                        r=ReportingObligation.objects.filter(country_id=c.id,reporting_obligation_type=i)
                        rep_count+=r.count()
                        r1=EventReporting.objects.filter(country_id=c.id,event_rep_type=i)
                        ev_count+=r1.count()
                    repC=(int)((rep_count * 100)/numb_countriesperregion)
                    reporting_array.append(repC)
                    repE=(int)((ev_count * 100)/numb_countriesperregion)
                    evreporting_array.append(repE)
                    if i==1:
                        regionrep1.append(reporting_array)   
                        context['region_rep'+str(i)]=regionrep1
                        regionev1.append(evreporting_array)   
                        context['region_ev'+str(i)]=regionev1
                    elif i==2:
                        regionrep2.append(reporting_array)   
                        context['region_rep'+str(i)]=regionrep2
                        regionev2.append(evreporting_array)   
                        context['region_ev'+str(i)]=regionev2
                    elif i==3:
                        regionrep3.append(reporting_array)   
                        context['region_rep'+str(i)]=regionrep3
                        regionev3.append(evreporting_array)   
                        context['region_ev'+str(i)]=regionev3
                    elif i==4:
                        regionrep4.append(reporting_array)   
                        context['region_rep'+str(i)]=regionrep4
                        regionev4.append(evreporting_array)   
                        context['region_ev'+str(i)]=regionev4
                    elif i==5:
                        regionev5.append(evreporting_array)   
                        context['region_ev'+str(i)]=regionev5    
                  #CP
                pests = []
                p_count=0
                for c in countriesperregioncp:
                    p=PestReport.objects.filter(country_id=c.id)
                    p_count+=p.count()
                pestC=(int)((p_count * 100)/numb_countriesperregioncp)
                pests.append(pestC)
                regionpestcp.append(pests)   
                context['region_pestcp']=regionpestcp

                for i in range(1,6):
                    rep_count=0
                    ev_count=0
                    reporting_array = []
                    evreporting_array=[]
                    for c in countriesperregioncp:
                        r=ReportingObligation.objects.filter(country_id=c.id,reporting_obligation_type=i)
                        rep_count+=r.count()
                        r1=EventReporting.objects.filter(country_id=c.id,event_rep_type=i)
                        ev_count+=r1.count()
                    repC=(int)((rep_count * 100)/numb_countriesperregioncp)
                    reporting_array.append(repC)
                    repE=(int)((ev_count * 100)/numb_countriesperregioncp)
                    evreporting_array.append(repE)
                    if i==1:
                        regionrep1cp.append(reporting_array)   
                        context['region_rep'+str(i)+'cp']=regionrep1cp
                        regionev1cp.append(evreporting_array)   
                        context['region_ev'+str(i)+'cp']=regionev1cp
                    elif i==2:
                        regionrep2cp.append(reporting_array)   
                        context['region_rep'+str(i)+'cp']=regionrep2cp
                        regionev2cp.append(evreporting_array)   
                        context['region_ev'+str(i)+'cp']=regionev2cp
                    elif i==3:
                        regionrep3cp.append(reporting_array)   
                        context['region_rep'+str(i)+'cp']=regionrep3cp
                        regionev3cp.append(evreporting_array)   
                        context['region_ev'+str(i)+'cp']=regionev3cp
                    elif i==4:
                        regionrep4cp.append(reporting_array)   
                        context['region_rep'+str(i)+'cp']=regionrep4cp
                        regionev4cp.append(evreporting_array)   
                        context['region_ev'+str(i)+'cp']=regionev4cp
                    elif i==5:
                        regionev5cp.append(evreporting_array)   
                        context['region_ev'+str(i)+'cp']=regionev5cp
                   #NCP
                pests = []
                p_count=0
                for c in countriesperregionncp:
                    p=PestReport.objects.filter(country_id=c.id)
                    p_count+=p.count()
                pestC=0
                if numb_countriesperregionncp>0:
                    pestC=(int)((p_count * 100)/numb_countriesperregionncp)
                pests.append(pestC)
                regionpestncp.append(pests)   
                context['region_pestncp']=regionpestncp

                for i in range(1,6):
                    rep_count=0
                    ev_count=0
                    reporting_array = []
                    evreporting_array=[]
                    for c in countriesperregionncp:
                        r=ReportingObligation.objects.filter(country_id=c.id,reporting_obligation_type=i)
                        rep_count+=r.count()
                        r1=EventReporting.objects.filter(country_id=c.id,event_rep_type=i)
                        ev_count+=r1.count()
                    repC=0
                    repE=0
                    if numb_countriesperregionncp>0:
                        repC=(int)((rep_count * 100)/numb_countriesperregionncp)
                        repE=(int)((ev_count * 100)/numb_countriesperregionncp)
              
                    reporting_array.append(repC)
                    evreporting_array.append(repE)
                    if i==1:
                        regionrep1ncp.append(reporting_array)   
                        context['region_rep'+str(i)+'ncp']=regionrep1ncp
                        regionev1ncp.append(evreporting_array)   
                        context['region_ev'+str(i)+'ncp']=regionev1ncp
                    elif i==2:
                        regionrep2ncp.append(reporting_array)   
                        context['region_rep'+str(i)+'ncp']=regionrep2ncp
                        regionev2ncp.append(evreporting_array)   
                        context['region_ev'+str(i)+'ncp']=regionev2ncp
                    elif i==3:
                        regionrep3ncp.append(reporting_array)   
                        context['region_rep'+str(i)+'ncp']=regionrep3ncp
                        regionev3ncp.append(evreporting_array)   
                        context['region_ev'+str(i)+'ncp']=regionev3ncp
                    elif i==4:
                        regionrep4ncp.append(reporting_array)   
                        context['region_rep'+str(i)+'ncp']=regionrep4ncp
                        regionev4ncp.append(evreporting_array)   
                        context['region_ev'+str(i)+'ncp']=regionev4ncp
                    elif i==5:
                        regionev5ncp.append(evreporting_array)   
                        context['region_ev'+str(i)+'ncp']=regionev5ncp
  
        return context

class CountryRegionsUsersListView(ListView):
    """   Statistic users per regions  """
    context_object_name = 'latest'
    model = CountryPage
    template_name = 'countries/countries_regionsusers.html'
    queryset = CountryPage.objects.all().order_by('title')
   
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(CountryRegionsUsersListView, self).get_context_data(**kwargs)
        context['dategenerate']=timezone.now()
    
        regionCNcp = []
        regionCNncp = []
        regionall= []
        regionOffcp = []
        regionUnOffcp = []
        regionInfoncp = []
        regionLocalncp = []
        regionEditors = []
        
        
        tot_o_count=1       
        tot_u_count=1       
        tot_i_count=1       
        tot_l_count=1       
        tot_e_count=1       
        for k,v in REGIONS:
            reg = v.lower()
            numCNcp = []
            countriesperregioncp=CountryPage.objects.filter(region=k,cp_ncp_t_type='CP')
            numb_countriesperregioncp=countriesperregioncp.count()
            numCNcp.append(reg)
            numCNcp.append(numb_countriesperregioncp)
            regionCNcp.append(numCNcp)
            context['region_cp']=regionCNcp

            numCNncp = []
            countriesperregionncp=CountryPage.objects.filter(region=k,cp_ncp_t_type='NCP')
            numb_countriesperregionncp=countriesperregionncp.count()
            numCNncp.append(reg)
            numCNncp.append(numb_countriesperregionncp)
            regionCNncp.append(numCNncp)
            context['region_ncp']=regionCNncp
            
            numAll = []
            numAll.append(reg)
            numAll.append(numb_countriesperregioncp+numb_countriesperregionncp)
            regionall.append(numAll)
            context['regions']=regionall

            official = []
            unofficial = []
            infopoint = []
            local = []
            editors = []
            
            o_count=0
            u_count=0
            i_count=0
            l_count=0
            e_count=0
            #CP
            for c in countriesperregioncp:
                o_count+=IppcUserProfile.objects.filter(country=c.id,contact_type='1').count()
                u_count+=IppcUserProfile.objects.filter(country=c.id,contact_type='2').count()
                e_count+=IppcUserProfile.objects.filter(country=c.id,contact_type='5').count()
            official.append(o_count)
            regionOffcp.append(official)   
            context['region_off_cp']=regionOffcp
            unofficial.append(u_count)
            regionUnOffcp.append(unofficial)   
            context['region_unoff_cp']=regionUnOffcp
            tot_o_count+=o_count
            tot_e_count+=e_count
            tot_u_count+=u_count
            
            #NCP
            for c in countriesperregionncp:
                i_count+=IppcUserProfile.objects.filter(country=c.id,contact_type='3').count()
                l_count+=IppcUserProfile.objects.filter(country=c.id,contact_type='4').count()
                e_count+=IppcUserProfile.objects.filter(country=c.id,contact_type='5').count()
            infopoint.append(i_count)
            regionInfoncp.append(infopoint)   
            context['region_info_ncp']=regionInfoncp
            local.append(l_count)
            regionLocalncp.append(local)   
            context['region_local_ncp']=regionLocalncp
            editors.append(e_count)
            regionEditors.append(editors)   
            context['region_editors']=regionEditors
            tot_i_count+=i_count
            tot_l_count+=l_count
            tot_e_count+=e_count
            
        context['tot_o_count']=tot_o_count       
        context['tot_u_count']=tot_u_count       
        context['tot_i_count']=tot_i_count       
        context['tot_l_count']=tot_l_count       
        context['tot_e_count']=tot_e_count       
        
        datachart1=''
        datachart2=''
        datachart3=''
        datachart4=''
        datachart5=''
        for k,v in REGIONS:
           datachart1 += ' {  y: '+str(regionOffcp[k-1][0]*100/tot_o_count)+', legendText:"'+str(v.__unicode__())+'", label: "'+str(v.__unicode__())+': '+str(regionOffcp[k-1][0]*100/tot_o_count)+'%" },'
           datachart2 += ' {  y: '+str(regionUnOffcp[k-1][0]*100/tot_u_count)+', legendText:"'+str(v.__unicode__())+'", label: "'+str(v.__unicode__())+': '+str(regionUnOffcp[k-1][0]*100/tot_u_count)+'%" },'
           datachart3 += ' {  y: '+str(regionInfoncp[k-1][0]*100/tot_i_count)+', legendText:"'+str(v.__unicode__())+'", label: "'+str(v.__unicode__())+': '+str(regionInfoncp[k-1][0]*100/tot_i_count)+'%" },'
           datachart4 += ' {  y: '+str(regionLocalncp[k-1][0]*100/tot_l_count)+', legendText:"'+str(v.__unicode__())+'", label: "'+str(v.__unicode__())+': '+str(regionLocalncp[k-1][0]*100/tot_l_count)+'%" },'
           datachart5 += ' {  y: '+str(regionEditors[k-1][0]*100/tot_e_count)+', legendText:"'+str(v.__unicode__())+'", label: "'+str(v.__unicode__())+': '+str(regionEditors[k-1][0]*100/tot_e_count)+'%" },'

        context['datachart1']=datachart1       
        context['datachart2']=datachart2       
        context['datachart3']=datachart3       
        context['datachart4']=datachart4       
        context['datachart5']=datachart5       
        return context

from datetime import date


class CountryTotalUsersListView(ListView):
    """    Statistic status of ippc contact points,editors,users  """
    context_object_name = 'latest'
    model = CountryPage
    template_name = 'countries/countries_totalusers.html'
    queryset = CountryPage.objects.all().order_by('title')
   
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(CountryTotalUsersListView, self).get_context_data(**kwargs)
        context['dategenerate']=timezone.now()
        
        context['tot_o_count']=IppcUserProfile.objects.filter(contact_type='1').count()
        context['tot_u_count']=IppcUserProfile.objects.filter(contact_type='2').count()
        context['tot_i_count']=IppcUserProfile.objects.filter(contact_type='3').count()
        context['tot_l_count']=IppcUserProfile.objects.filter(contact_type='4').count()
        context['tot_e_count']=IppcUserProfile.objects.filter(contact_type='5').count()
        context['tot_users']=IppcUserProfile.objects.filter().count()
        context['tot_users']=IppcUserProfile.objects.filter().count()
        context['tot_users']=IppcUserProfile.objects.filter().count()
        timezone.now()
       
        curryear=timezone.now().year
        date1=datetime(curryear-2, 12, 31,23,59,00)
        date2=datetime(curryear-1, 12, 31,23,59,00)
        context['date1']=curryear-2
        context['date2']=curryear-1
      
        u_date1=IppcUserProfile.objects.filter(date_account_created__lte=date1).count()
        u_date2=IppcUserProfile.objects.filter(date_account_created__gte=date1,date_account_created__lte=date2).count()

        u_percentage=0
        if u_date1>0:
            u_precentage=u_date2*100/u_date1
        context['u_date1']=u_date1
        context['u_date2']=u_date2
        context['u_percentage']=u_percentage
        
        new_content1=0#modify_date
        new_content1+=EventReporting.objects.filter(publish_date__lte=date1).count()
        new_content1+=ReportingObligation.objects.filter(publish_date__lte=date1).count()
        new_content1+=PestReport.objects.filter(publish_date__lte=date1).count()
        new_content1+=ImplementationISPM.objects.filter(publish_date__lte=date1).count()
        new_content1+=PestFreeArea.objects.filter(publish_date__lte=date1).count()
        new_content1+=Website.objects.filter(publish_date__lte=date1).count()
        new_content1+=CnPublication.objects.filter(publish_date__lte=date1).count()
        new_content1+=CountryNews.objects.filter(publish_date__lte=date1).count()
      
        new_content2=0#modify_date
        new_content2+=EventReporting.objects.filter(publish_date__lte=date2,publish_date__gte=date1).count()
        new_content2+=ReportingObligation.objects.filter(publish_date__lte=date2,publish_date__gte=date1).count()
        new_content2+=PestReport.objects.filter(publish_date__lte=date2,publish_date__gte=date1).count()
        new_content2+=ImplementationISPM.objects.filter(publish_date__lte=date2,publish_date__gte=date1).count()
        new_content2+=PestFreeArea.objects.filter(publish_date__lte=date2,publish_date__gte=date1).count()
        new_content2+=Website.objects.filter(publish_date__lte=date2,publish_date__gte=date1).count()
        new_content2+=CnPublication.objects.filter(publish_date__lte=date2,publish_date__gte=date1).count()
        new_content2+=CountryNews.objects.filter(publish_date__lte=date2,publish_date__gte=date1).count()
        
        new_content_percentage=0
        if new_content1>0:
            new_content_percentage=new_content2*100/new_content1
        context['new_content1']=new_content1
        context['new_content2']=new_content2
        context['new_content_percentage']=new_content_percentage
        
        up_content1=0#modify_date
        up_content1+=EventReporting.objects.filter(modify_date__lte=date1).count()
        up_content1+=ReportingObligation.objects.filter(modify_date__lte=date1).count()
        up_content1+=PestReport.objects.filter(modify_date__lte=date1).count()
        up_content1+=ImplementationISPM.objects.filter(modify_date__lte=date1).count()
        up_content1+=PestFreeArea.objects.filter(modify_date__lte=date1).count()
        up_content1+=Website.objects.filter(modify_date__lte=date1).count()
        up_content1+=CnPublication.objects.filter(modify_date__lte=date1).count()
        up_content1+=CountryNews.objects.filter(modify_date__lte=date1).count()
      
        up_content2=0#modify_date
        up_content2+=EventReporting.objects.filter(modify_date__lte=date2,modify_date__gte=date1).count()
        up_content2+=ReportingObligation.objects.filter(modify_date__lte=date2,modify_date__gte=date1).count()
        up_content2+=PestReport.objects.filter(modify_date__lte=date2,modify_date__gte=date1).count()
        up_content2+=ImplementationISPM.objects.filter(modify_date__lte=date2,modify_date__gte=date1).count()
        up_content2+=PestFreeArea.objects.filter(modify_date__lte=date2,modify_date__gte=date1).count()
        up_content2+=Website.objects.filter(modify_date__lte=date2,modify_date__gte=date1).count()
        up_content2+=CnPublication.objects.filter(modify_date__lte=date2,modify_date__gte=date1).count()
        up_content2+=CountryNews.objects.filter(modify_date__lte=date2,modify_date__gte=date1).count()
        
        up_content_percentage=0
        if up_content1>0:
            up_content_percentage=up_content2*100/up_content1
        context['up_content1']=up_content1
        context['up_content2']=up_content2
        context['up_content_percentage']=up_content_percentage
       
            
        return context


class PollListView(ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'
    def get_queryset(self):
        """Return the last five published polls."""
        return Poll.objects.order_by('-pub_date').all


class PollDetailView(DetailView):
    model = Poll
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """Return the last five published polls."""
        return Poll.objects.filter(pub_date__lte=timezone.now())
        

class PollResultsView(DetailView):
    model = Poll
    template_name = 'polls/results.html'
    
    def get_context_data(self, **kwargs):
        context = super(PollResultsView, self).get_context_data(**kwargs)
        pollid=self.kwargs['pk']
        votes=PollVotes.objects.filter(poll_id=pollid)
        context['votes']= votes
        return context

def send_pollnotification_message(id):
    """ send_pollnotification_message """
    #send notification to SC
    poll = get_object_or_404(Poll,  pk=id)
    emailto_all = ['']
    for g in Group.objects.filter(id=4):
        users = g.user_set.all()
        for u in users:
           user_obj=User.objects.get(username=u)
           emailto_all.append(str(user_obj.email))
    subject='IPPC POLL:  new poll: '+poll.question
    textmessage='<p>Dear IPPC user,<br><br>a new poll has been posted and it is open for your answer ( selecting YES or NO) and comments:<br>    <br>Poll: '+poll.question+'<br><br>'+poll.polltext+'<br><br>You can view it at the following url: https://www.ippc.int/poll/'+str(id)+'<br><br>International Plant Protection Convention team </p>'

    #message = mail.EmailMessage(subject,textmessage,'paola.sentinelli@fao.org',#from
    #    ['paola.sentinelli@fao.org',], ['paola.sentinelli@fao.org'])#emailto_all for PROD, in TEST all to paola#
    message = mail.EmailMessage(subject,textmessage,'ippc@fao.org',#from
        [emailto_all], ['paola.sentinelli@fao.org'])#emailto_all for PROD, in TEST all to paola#
    
    message.content_subtype = "html"
    # sent =message.send()
        
        


@login_required
@permission_required('ippc.add_poll', login_url="/accounts/login/")
def poll_create(request):
    """ Create Poll """
    user = request.user
    author = user

    form = PollForm(request.POST)
    if request.method == "POST":
         c_form = Poll_ChoiceFormSet(request.POST)
         if form.is_valid() and c_form.is_valid():
            new_poll = form.save(commit=False)
            form.save()
           
            c_form.instance = new_poll
            c_form.save()
            # send_pollnotification_message(new_poll.id)
            
            info(request, _("Successfully created Poll."))
            return redirect("detail", pk=new_poll.id)
         else:
             return render_to_response('polls/poll_create.html', {'form': form,'c_form': c_form,},
             context_instance=RequestContext(request))
       
    else:
        form = PollForm( instance=Poll())
        c_form =Poll_ChoiceFormSet()
    return render_to_response('polls/poll_create.html', {'form': form,'c_form': c_form},
        context_instance=RequestContext(request))

@login_required
@permission_required('ippc.change_poll', login_url="/accounts/login/")
def poll_edit(request, id=None, template_name='polls/poll_edit.html'):
    """ Edit Poll """
    if id:
        poll = get_object_or_404(Poll,  pk=id)
    else:
        poll = Poll()
      
    if request.POST:

        form =PollForm(request.POST, instance=poll)
        c_form = Poll_ChoiceFormSet(request.POST,  instance=poll)
        if form.is_valid() and c_form.is_valid():
            form.save()
            c_form.instance = poll
            c_form.save()
            send_pollnotification_message(id)

            return redirect("detail", pk=id)
    else:
        form = PollForm(instance=poll)
        c_form = Poll_ChoiceFormSet(instance=poll)
        
    return render_to_response(template_name, {
        'form': form,'c_form':c_form, "poll": poll
    }, context_instance=RequestContext(request))
    
        
def vote_poll(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    if PollVotes.objects.filter(poll_id=poll_id, user_id=request.user.id).exists():
        return render(request, 'polls/detail.html', {
        'poll': p,
        'error_message': "Sorry, but you have already voted."
        })
    try:
        selected_choice = p.poll_choice_set.get(pk=request.POST['choice'])
    except (KeyError, Poll_Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        v = PollVotes(user=request.user, poll=p,choice=selected_choice,comment=request.POST['comment'])
        v.save()
        return redirect("results", pk=p.id)

class EmailUtilityMessageListView(ListView):
    """    EmailUtilityMessage List view """
    context_object_name = 'latest'
    model = EmailUtilityMessage
    date_field = 'date'
    template_name = 'emailutility/emailutility_list.html'
    queryset = EmailUtilityMessage.objects.all().order_by('-date', 'subject')
   
       
class EmailUtilityMessageDetailView(DetailView):
    """ EmailUtilityMessage detail page """
    model = EmailUtilityMessage
    context_object_name = 'emailmessage'
    template_name = 'emailutility/emailutility_detail.html'
    queryset = EmailUtilityMessage.objects.filter()

def split(arr, size):
     arrs = []
     while len(arr) > size:
         pice = arr[:size]
         arrs.append(pice)
         arr   = arr[size:]
     arrs.append(arr)
     return arrs
 
@login_required
@permission_required('ippc.add_emailutilitymessage', login_url="/accounts/login/")
def email_send(request):
    """ Create email to send """
    form = EmailUtilityMessageForm(request.POST)
    
    g_set=[]
    for g in Group.objects.filter():
        users = g.user_set.all()
        users_all=[]
        users_all.append(str(g))
        users_all.append(str(g.id))
        for u in users:
           users_u=[]
           user_obj=User.objects.get(username=u)
           userippc = get_object_or_404(IppcUserProfile, user_id=user_obj.id)
           users_u.append((unicode(userippc.first_name)))
           users_u.append((unicode(userippc.last_name)))
           users_u.append((user_obj.email))
           users_all.append(users_u)
        g_set.append(users_all)
    
    users_all=[]
 
    cp_set0=[]
    users_all=[]
    cp=IppcUserProfile.objects.filter(contact_type=1)
    cpname = get_object_or_404(ContactType,id=1)
    for u in cp:
           users_u=[]
           user_obj=User.objects.get(id=u.user_id)
           cn = get_object_or_404(CountryPage,id=u.country_id)
           users_u.append(str(cn))
           users_u.append(' ('+(unicode(u.first_name))+' '+(unicode(u.last_name))+') ')
           users_u.append(str(user_obj.email))
           users_all.append(users_u)
           
    users_all2= split(users_all,30)   
    j=0
    users_all_2=[]
    for xx in users_all2:
        users_all_2=[]
       
        k=j+1
        users_all_2.append(str(cpname)+" - Group "+str(k))
        users_all_2.append(str(j))
        j=j+1
        for x in xx:
            users_all_2.append(x)
    
        cp_set0.append(users_all_2)
        
    
   
    cp_set=[]      
    for h in range(2,5):
        users_all=[]
        cp=IppcUserProfile.objects.filter(contact_type=h)
        cpname = get_object_or_404(ContactType,id=h)
        users_all.append(str(cpname))
        users_all.append(str(h))
        cp=IppcUserProfile.objects.filter(contact_type=h)
        for u in cp:
               users_u=[]
               user_obj=User.objects.get(id=u.user_id)
               cn = get_object_or_404(CountryPage,id=u.country_id)
               users_u.append(str(cn))
               users_u.append(' ('+(unicode(u.first_name))+' '+(unicode(u.last_name))+') ')
               users_u.append(str(user_obj.email))
               users_all.append(users_u)

        cp_set.append(users_all)


    if request.method == "POST":
        f_form =EmailUtilityMessageFileFormSet(request.POST, request.FILES)
        if form.is_valid() and f_form.is_valid():
            emailto_all = [str(request.POST['emailto'])]
            for u in request.POST.getlist('users'):
                user_obj=User.objects.get(id=u)
                user_email=user_obj.email
                emailto_all.append(str(user_email))
            for g in Group.objects.filter():
                for uemail in request.POST.getlist('user_'+str(g.id)+'_0'):
                    emailto_all.append(str(uemail))
                    
            for h in range(2,5):
                  for uemail in request.POST.getlist('usercp_'+str(h)+'_0'):
                     emailto_all.append(str(uemail))
            for h in range(0,6):
                  for uemail in request.POST.getlist('usercp1_'+str(h)+'_0'):
                     emailto_all.append(str(uemail))                     
            #print(emailto_all)
            new_emailmessage = form.save(commit=False)
            new_emailmessage.date=timezone.now()
            new_emailmessage.emailto=emailto_all
            form.save()
            #save file to message in db
            f_form.instance = new_emailmessage
            f_form.save()
            #EmailMessage('Hello', 'Body goes here', 'from@example.com', ['to1@example.com', 'to2@example.com'], ['bcc@example.com'],  headers = {'Reply-To': 'another@example.com'})
            #send email message
            #message = mail.EmailMessage(request.POST['subject'],request.POST['messagebody'],request.POST['emailfrom'],
            #['paola.sentinelli@fao.org',], ['paola.sentinelli@fao.org'])#emailto_all for PROD, in TEST all to paola#
            emailto_all_split=[]
            #print('================================')
            #print(emailto_all)
            #print('================================')
            #if len(emailto_all) >30 :
            emailto_all_split = split(emailto_all,30)
            sent =0
            for emails_arr in emailto_all_split:
                messages=[]
                for emails_a in emails_arr:
                    message = mail.EmailMessage(request.POST['subject'],request.POST['messagebody'],request.POST['emailfrom'],
                    [emails_a], ['paola.sentinelli@fao.org'])#emailto_all for PROD, in TEST all to paola#
                    #print('===*******SENDING**********===')
                    #print (emails_arr)
                    #print('====******************************===')
                    # Attach a files to message
                    fileset= EmailUtilityMessageFile.objects.filter(emailmessage_id=new_emailmessage.id)
                    for f in fileset:
                        pf=MEDIA_ROOT+str(f.file)
                        message.attach_file(pf) 
                    message.content_subtype = "html"
                    messages.append(message)
                    #timeout, so changed to send_messages
                    #sent =message.send()
                # Manually open the connection
                #sends a list of EmailMessage objects. If the connection is not open, this call will implicitly open the connection, and close the connection afterwards. If the connection is already open, it will be left open after mail has been sent.
                connection = mail.get_connection()
                connection.open()
                sent=connection.send_messages(messages)
                connection.close()
               
            #update status SENT/NOT SENT mail message in db
            new_emailmessage.sent=sent
            form.save()
           
            info(request, _("Email  sent."))
            return redirect("email-detail",new_emailmessage.id)
        else:
             return render_to_response('emailutility/emailutility_send.html', {'form': form,'f_form': f_form,'emailgroups':g_set,'emailcp':cp_set,'emailcp2':cp_set0},
             context_instance=RequestContext(request))
    else:
        form = EmailUtilityMessageForm(instance=EmailUtilityMessage())
        f_form =EmailUtilityMessageFileFormSet()
      
    return render_to_response('emailutility/emailutility_send.html', {'form': form  ,'f_form': f_form,'emailgroups':g_set,'emailcp':cp_set,'emailcp2':cp_set0,},#'emailcpu':cpu_set,'emailcpi':cpi_set,'emailcpl':cpl_set
        context_instance=RequestContext(request))

   


class AdvancesSearchCNListView(ListView):
    """  AdvancesSearchCNListView list  """
    context_object_name = 'latest'
    model = CountryPage
    template_name = 'countries/countries_advsearchresults.html'
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(AdvancesSearchCNListView, self).get_context_data(**kwargs)
        if self.kwargs['type'] == 'pestreport':
            context['type_label'] = 'Official pest report (Art. VIII.1a)'
            context['link_to_item'] = 'pest-report-detail'
            context['items']= PestReport.objects.all()
            context['counttotal'] =context['items'].count() 
           
            cns= CountryPage.objects.all()
            maparray=[]
            maparray1=""
            tot_p=0
            for cn in cns:
              pests=PestReport.objects.filter(country_id=cn.id)
              p=pests.count()
              tot_p+=p
              if p>0:
                  if cn>0:
                    maparray.append([str('<a href="/'+cn.country_slug+'/pestreports/">'+cn.name)+': '+str(p)+'</a>',str(cn.cn_lat),str(cn.cn_long)])
                    maparray1+='citymap[\''+str(cn.country_slug)+'\'] = {center: new google.maps.LatLng('+str(cn.cn_lat)+','+str(cn.cn_long)+'), text:\''+str(cn.name)+': '+str(p)+''+'\', html:\''+str('<a href="/'+cn.country_slug+'/pestreports/">'+cn.name)+': '+str(p)+'</a>'+'\',  population:' +str(p)+'};'
              
            context['map']=maparray
            context['map1']=maparray1
            
        if self.kwargs['type'] == 'pestreportstat':
            context['type_label'] = 'Official pest report (Art. VIII.1a)'
            context['item'] = 'pestreportstat'
            context['link_to_item'] = 'pest-report-detail'
            arrayGen={'1ANIMK':'Animalia;',
                      '1ARCAK':'Archaea;',
                      '1BACTK':'Bacteria;',
                      '1CHROK':'Chromista;',
                      '1FUNGK':'Fungi;',
                      '1PLAK':'Plantae;',
                      '1PROTK':'Protozoa;',
                      '1VIRUK':'Viruses and viroids;'}
            cns= CountryPage.objects.all()
          
            tot_p=0
            for cn in cns:
              pests=PestReport.objects.filter(country_id=cn.id)
              p=pests.count()
              tot_p+=p
              for pp in pests:
                  e=EppoCode.objects.filter(codename=pp.pest_identity)
                  if e:
                    ecode=e[0].code
                    codeparent=e[0].codeparent
                    for h in range(1,10):
                          e1=EppoCode.objects.filter(code=codeparent)
                          if(e1.count()>0):
                             if(e1[0].codeparent=='null'):
                                   break
                             else:
                                  ecode=e1[0].code
                                  codeparent=e1[0].codeparent
                                  h=h+1
                    
                    aaa=arrayGen[codeparent]
                    aaa+=str(pp.id)+'*'
                    arrayGen[codeparent]=aaa
                   
            
            datachart=''
               
            for h in arrayGen:
                s=arrayGen[h].split(';');
                values=s[1].split('*');
                val=len(values)-1
                perc=0
                if tot_p>0:
                    perc=(val*100/ tot_p)
                datachart+= ' {  y: '+str(perc)+', legendText:"'+s[0]+'", label: "'+s[0]+' '+str(perc)+'%" },'
            context['datachart']=datachart

            
        elif self.kwargs['type'] == 'contactpoints':
            context['type_label'] = 'Contact points'
            context['users']=User.objects.all()
            context['cns']=CountryPage.objects.all()
         
            context['items']=IppcUserProfile.objects.filter(contact_type='1')|IppcUserProfile.objects.filter(contact_type='2')|IppcUserProfile.objects.filter(contact_type='3')|IppcUserProfile.objects.filter(contact_type='4')
            context['counttotal'] =context['items'].count() 
            context['link_to_item'] = 'contactpoint'
                 
        elif self.kwargs['type'] == 'nppo':
            context['type_label'] = dict(BASIC_REP_TYPE_CHOICES)[1]
            context['link_to_item'] = 'reporting-obligation-detail'
            context['items']= ReportingObligation.objects.filter(reporting_obligation_type=1)
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'entrypoints':
            context['type_label'] = dict(BASIC_REP_TYPE_CHOICES)[2]
            context['link_to_item'] = 'reporting-obligation-detail'
            context['items']= ReportingObligation.objects.filter(reporting_obligation_type=2)
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'regulatedpests':
            context['type_label'] = dict(BASIC_REP_TYPE_CHOICES)[3]
            context['link_to_item'] = 'reporting-obligation-detail'
            context['items']= ReportingObligation.objects.filter(reporting_obligation_type=3)
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'legislation':
            context['type_label'] = dict(BASIC_REP_TYPE_CHOICES)[4]
            context['link_to_item'] = 'reporting-obligation-detail'
            context['items']= ReportingObligation.objects.filter(reporting_obligation_type=4)
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'emergencyactions':
            context['type_label'] = dict(EVT_REP_TYPE_CHOICES)[1]
            context['link_to_item'] = 'event-reporting-detail'
            context['items']= EventReporting.objects.filter(event_rep_type=1)
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'noncompliance':
            context['type_label'] = dict(EVT_REP_TYPE_CHOICES)[2]
            context['link_to_item'] = 'event-reporting-detail'
            context['items']= EventReporting.objects.filter(event_rep_type=2)
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'plantprotection':
            context['type_label'] = dict(EVT_REP_TYPE_CHOICES)[3]
            context['link_to_item'] = 'event-reporting-detail'
            context['items']= EventReporting.objects.filter(event_rep_type=3)
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'peststatus':
            context['type_label'] = dict(EVT_REP_TYPE_CHOICES)[4]
            context['link_to_item'] = 'event-reporting-detail'
            context['items']= EventReporting.objects.filter(event_rep_type=4)
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'phytosanitaryrequirements':
            context['type_label'] = dict(EVT_REP_TYPE_CHOICES)[5]
            context['link_to_item'] = 'event-reporting-detail'
            context['items']= EventReporting.objects.filter(event_rep_type=5)
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'pfa':
            context['type_label'] = 'Pest free areas'
            context['link_to_item'] = 'pfa-detail'
            context['items']= PestFreeArea.objects.all()
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'ispm15':
            context['type_label'] = 'Implementation of ISPM 15'
            context['link_to_item'] = 'implementationispm-detail'
            context['items']= ImplementationISPM.objects.all()
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'countrynews':
            context['type_label'] = 'Country news'
            context['link_to_item'] = 'country-news-detail'
            context['items']= CountryNews.objects.all()
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'countrywebsites':
            context['type_label'] = 'Country websites'
            context['link_to_item'] = 'website-detail'
            context['items']= Website.objects.all()
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'cnpublication':
            context['type_label'] = 'Country publication'
            context['link_to_item'] = 'country-publication-detail'
            context['items']= CnPublication.objects.all()
            context['counttotal'] =context['items'].count() 
         
        return context
import csv
from django.http import HttpResponse	

def contactPointExtractor(request):
    # Create the HttpResponse object with the appropriate CSV header.
    contacts=IppcUserProfile.objects.filter(contact_type='1')|IppcUserProfile.objects.filter(contact_type='2')|IppcUserProfile.objects.filter(contact_type='3')|IppcUserProfile.objects.filter(contact_type='4')
    users=User.objects.all()
    cns=CountryPage.objects.all()
             
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contactpoints.csv"'

    writer = csv.writer(response)
    writer.writerow(['Country', 'Contact Type', 'Prefix', 'First Name','Last Name','Email','Alternate E-mail','Address'])
   
    for c in contacts:
        country=''
        c_type=''
        for cn in cns:          
            if cn.id == c.country_id:
               country = cn
        print (c.contact_type)      
        for o in c.contact_type.all():
            c_type=o
        c_gender=c.gender
        c_first_name= c.first_name
        c_last_name= c.last_name
        c_email=''
        for u in users:
            if u.id == c.user_id:
              u.email
        c_emailalt =c.email_address_alt
        c_address=c.address1
        
        writer.writerow([country,c_type,c_gender, c_first_name.encode('utf-8'), c_last_name.encode('utf-8'),c_email,c_emailalt,c_address.encode('utf-8')])

    return response	

def draftprotocol_compilecomments(request,id=None):
    # Create the HttpResponse object with the appropriate CSV header.
       response = HttpResponse(content_type='text/csv')
       response['Content-Disposition'] = 'attachment; filename="compiled_comments_DP_'+timezone.now().strftime('%Y%m%d%H%M%S')+'.csv"'
       writer = csv.writer(response)
       writer.writerow(['Author','Expertise On This Pest','Institution','Comment','Attachments'])
       draftprotocol = get_object_or_404(DraftProtocol,  pk=id)
       queryset = DraftProtocolComments.objects.filter(draftprotocol_id=draftprotocol.id)
     
         
       for obj in queryset:
            author=''
            expertise=''
            intitution=''
            comment=''
            attch=''
            attch2=''
            lastdate=''
            
            author=obj.author
            expertise=obj.expertise
            intitution=obj.institution
            comment=obj.comment
            attch=obj.filetext
            attch2=obj.filefig
            writer.writerow([author,expertise.encode('utf-8'),intitution.encode('utf-8'), comment.encode('utf-8'), attch,attch2])

       return response	

	
