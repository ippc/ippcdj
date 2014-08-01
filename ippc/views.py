from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages import info, error
from django.utils import timezone
from django.core import mail
from django.conf import settings
from django.contrib.auth.models import User,Group
from .models import EmailUtilityMessage, EmailUtilityMessageFile, Poll_Choice, Poll,PollVotes, IppcUserProfile,CountryPage, PestStatus, PestReport, IS_PUBLIC, IS_HIDDEN, Publication,\
ReportingObligation, BASIC_REP_TYPE_CHOICES, EventReporting, EVT_REP_TYPE_CHOICES,Website,CnPublication,CountryNews, \
PestFreeArea,ImplementationISPM,REGIONS, IssueKeywordsRelate,CommodityKeywordsRelate,EventreportingFile,ReportingObligation_File
from mezzanine.core.models import Displayable, CONTENT_STATUS_DRAFT, CONTENT_STATUS_PUBLISHED
from .forms import PestReportForm, ReportingObligationForm, EventReportingForm, PestFreeAreaForm,\
ImplementationISPMForm,IssueKeywordsRelateForm,CommodityKeywordsRelateForm,EventreportingFileFormSet,ReportingoblicationFileFormSet,\
ImplementationISPMFileFormSet,PestFreeAreaFileFormSet, PestReportFileFormSet,WebsiteUrlFormSet,WebsiteForm, \
EventreportingUrlFormSet, ReportingObligationUrlFormSet ,PestFreeAreaUrlFormSet,ImplementationISPMUrlFormSet,PestReportUrlFormSet,\
CnPublicationUrlFormSet,CnPublicationForm, CnPublicationFileFormSet,EmailUtilityMessageForm,EmailUtilityMessageFileFormSet,\
CountryNewsUrlFormSet,CountryNewsForm, CountryNewsFileFormSet

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
def get_profile():
    return IppcUserProfile.objects.all()

# def pest_report_country():
#     return PestReport.objects.all()
    
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
    paginate_by = 30

class PublicationDetailView(DetailView):
    """ Publication detail page """
    model = Publication
    context_object_name = 'publication'
    template_name = 'pages/publication_detail.html'
    queryset = Publication.objects.filter(status=IS_PUBLIC)


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
        
    countryo = get_object_or_404(CountryPage, name=country)
    numberR=PestReport.objects.filter(country__country_slug=country).count()
    numberR=numberR+1
    pestnumber=str(numberR)
    if numberR<10 :
        pestnumber='0'+pestnumber
    report_number_val=countryo.iso3+'-'+pestnumber+'/1'
    print   (report_number_val)     
   
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
            
            f_form.instance = new_pest_report
            f_form.save()
            u_form.instance = new_pest_report
            u_form.save()
            info(request, _("Successfully created pest report."))
            
            if new_pest_report.status == CONTENT_STATUS_DRAFT:
                return redirect("pest-report-hidden-list", country=user_country_slug)
            else:
                return redirect("pest-report-detail", country=user_country_slug, year=new_pest_report.publish_date.strftime("%Y"), month=new_pest_report.publish_date.strftime("%m"), slug=new_pest_report.slug)
         else:
             return render_to_response('countries/pest_report_create.html', {'form': form,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform},
             context_instance=RequestContext(request))
       
    else:
        form = PestReportForm(initial={'country': country}, instance=PestReport())
        issueform =IssueKeywordsRelateForm(request.POST)
        commodityform =CommodityKeywordsRelateForm(request.POST)
        f_form =PestReportFileFormSet()
        u_form =PestReportUrlFormSet()
    return render_to_response('countries/pest_report_create.html', {'form': form,'f_form': f_form,'u_form':u_form,'issueform':issueform, 'commodityform':commodityform},
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
        issues = get_object_or_404(IssueKeywordsRelate, pk=pest_report.issuename.all()[0].id)
        commodities = get_object_or_404(CommodityKeywordsRelate, pk=pest_report.commname.all()[0].id)
        
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
        issueform =IssueKeywordsRelateForm(request.POST, instance=issues)
        commodityform =CommodityKeywordsRelateForm(request.POST, instance=commodities)
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
            
            f_form.instance = pest_report
            f_form.save()
            u_form.instance = pest_report
            u_form.save()
            # If the save was successful, success message and redirect to another page
            # info(request, _("Successfully updated pest report."))
            if pest_report.status == CONTENT_STATUS_DRAFT:
                return redirect("pest-report-hidden-list", country=user_country_slug)
            else:
                return redirect("pest-report-detail",country=user_country_slug, year=pest_report.publish_date.strftime("%Y"), month=pest_report.publish_date.strftime("%m"), slug=pest_report.slug)

    else:
        form = PestReportForm(instance=pest_report)
        issueform =IssueKeywordsRelateForm(instance=issues)
        commodityform =CommodityKeywordsRelateForm(instance=commodities)
        f_form = PestReportFileFormSet(instance=pest_report)
        u_form = PestReportUrlFormSet(instance=pest_report)
    return render_to_response(template_name, {
        'form': form,'f_form':f_form,'u_form':u_form,'issueform': issueform,'commodityform': commodityform,  "pest_report": pest_report
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
        # CountryPage country_slug == country URL parameter keyword argument
        return ReportingObligation.objects.filter(country__country_slug=self.country)
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(ReportingObligationListView, self).get_context_data(**kwargs)
        context['country'] = self.kwargs['country']
        context['basic_types'] =BASIC_REP_TYPE_CHOICES
        return context
   
       
   
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
            
            f_form.instance = new_reporting_obligation
            f_form.save()
            u_form.instance = new_reporting_obligation
            u_form.save()
            info(request, _("Successfully created Reporting obligation."))
            return redirect("reporting-obligation-detail", country=user_country_slug, year=new_reporting_obligation.publish_date.strftime("%Y"), month=new_reporting_obligation.publish_date.strftime("%m"), slug=new_reporting_obligation.slug)
         else:
            return render_to_response('countries/reporting_obligation_create.html', {'form': form,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform},
             context_instance=RequestContext(request))
    else:
        form = ReportingObligationForm(initial={'country': country,'reporting_obligation_type': type}, instance=ReportingObligation())
        issueform =IssueKeywordsRelateForm(request.POST)
        commodityform =CommodityKeywordsRelateForm(request.POST)
        f_form =ReportingoblicationFileFormSet()
        u_form =ReportingObligationUrlFormSet()

    return render_to_response('countries/reporting_obligation_create.html', {'form': form  ,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform},
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
        issues = get_object_or_404(IssueKeywordsRelate, pk=reporting_obligation.issuename.all()[0].id)
        commodities = get_object_or_404(CommodityKeywordsRelate, pk=reporting_obligation.commname.all()[0].id)
    else:
        reporting_obligation = ReportingObligation(author=request.user)
      
    if request.POST:
        form = ReportingObligationForm(request.POST, request.FILES, instance=reporting_obligation)
        issueform =IssueKeywordsRelateForm(request.POST, instance=issues)
        commodityform =CommodityKeywordsRelateForm(request.POST, instance=commodities)
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
            
            f_form.instance = reporting_obligation
            f_form.save()
            u_form.instance = reporting_obligation
            u_form.save()
            # If the save was successful, success message and redirect to another page

            info(request, _("Successfully updated Reporting obligation."))
            return redirect("reporting-obligation-detail", country=user_country_slug, year=reporting_obligation.publish_date.strftime("%Y"), month=reporting_obligation.publish_date.strftime("%m"), slug=reporting_obligation.slug)

    else:
        form = ReportingObligationForm(instance=reporting_obligation)
        issueform =IssueKeywordsRelateForm(instance=issues)
        commodityform =CommodityKeywordsRelateForm(instance=commodities)
        f_form = ReportingoblicationFileFormSet(instance=reporting_obligation)
        u_form = ReportingObligationUrlFormSet(instance=reporting_obligation)
    return render_to_response(template_name, {
        'form': form,'f_form':f_form,'u_form': u_form,'issueform': issueform,'commodityform': commodityform,  "reporting_obligation": reporting_obligation
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
        # CountryPage country_slug == country URL parameter keyword argument
        return EventReporting.objects.filter(country__country_slug=self.country)
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(EventReportingListView, self).get_context_data(**kwargs)
        context['country'] = self.kwargs['country']
        context['event_types'] =EVT_REP_TYPE_CHOICES
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
              
            f_form.instance = new_event_reporting
            f_form.save()
            u_form.instance = new_event_reporting
            u_form.save()
            info(request, _("Successfully added Event reporting."))
            return redirect("event-reporting-detail", country=user_country_slug, year=new_event_reporting.publish_date.strftime("%Y"), month=new_event_reporting.publish_date.strftime("%m"), slug=new_event_reporting.slug)
        else:
            return render_to_response('countries/event_reporting_create.html', {'form': form,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform},#'entryform': entryform,'docform':myformset,
             context_instance=RequestContext(request))

          
        
    else:
        form = EventReportingForm(initial={'country': country,'event_rep_type': type}, instance=EventReporting())
        issueform =IssueKeywordsRelateForm(request.POST)
        commodityform =CommodityKeywordsRelateForm(request.POST)
        f_form = EventreportingFileFormSet()
        u_form = EventreportingUrlFormSet()
    
    return render_to_response('countries/event_reporting_create.html', {'form': form,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform},
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
        issues = get_object_or_404(IssueKeywordsRelate, pk=event_reporting.issuename.all()[0].id)
        commodities = get_object_or_404(CommodityKeywordsRelate, pk=event_reporting.commname.all()[0].id)
    else:
        event_reporting = EventReporting(author=request.user)
      
    if request.POST:
        form = EventReportingForm(request.POST,  request.FILES, instance=event_reporting)
        issueform =IssueKeywordsRelateForm(request.POST,instance=issues)
        commodityform =CommodityKeywordsRelateForm(request.POST,instance=commodities)
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
    
            f_form.instance = event_reporting
            f_form.save()
            u_form.instance = event_reporting
            u_form.save()
            info(request, _("Successfully updated Event reporting."))
            return redirect("event-reporting-detail", country=user_country_slug, year=event_reporting.publish_date.strftime("%Y"), month=event_reporting.publish_date.strftime("%m"), slug=event_reporting.slug)

    else:
        form = EventReportingForm(instance=event_reporting)
        issueform =IssueKeywordsRelateForm(instance=issues)
        commodityform =CommodityKeywordsRelateForm(instance=commodities)
        f_form = EventreportingFileFormSet(instance=event_reporting)
        u_form = EventreportingUrlFormSet( instance=event_reporting)
      
    return render_to_response(template_name, {
        'form': form, 'f_form':f_form,'u_form': u_form,'issueform': issueform,  'commodityform': commodityform, "event_reporting": event_reporting
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
        issues = get_object_or_404(IssueKeywordsRelate, pk=website.issuename.all()[0].id)
        commodities = get_object_or_404(CommodityKeywordsRelate, pk=website.commname.all()[0].id)
    else:
        website = Website(author=request.user)
      
    if request.POST:
        form = WebsiteForm(request.POST,  request.FILES, instance=website)
        issueform =IssueKeywordsRelateForm(request.POST,instance=issues)
        commodityform =CommodityKeywordsRelateForm(request.POST,instance=commodities)
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
        issueform =IssueKeywordsRelateForm(instance=issues)
        commodityform =CommodityKeywordsRelateForm(instance=commodities)
        u_form = WebsiteUrlFormSet( instance=website)
      
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
        issues = get_object_or_404(IssueKeywordsRelate, pk=cnpublication.issuename.all()[0].id)
        commodities = get_object_or_404(CommodityKeywordsRelate, pk=cnpublication.commname.all()[0].id)
    else:
        cnpublication = CnPublication(author=request.user)
      
    if request.POST:
        form = CnPublicationForm(request.POST,  request.FILES, instance=cnpublication)
        issueform =IssueKeywordsRelateForm(request.POST,instance=issues)
        commodityform =CommodityKeywordsRelateForm(request.POST,instance=commodities)
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
        issueform =IssueKeywordsRelateForm(instance=issues)
        commodityform =CommodityKeywordsRelateForm(instance=commodities)
        f_form = CnPublicationFileFormSet(instance=cnpublication)
        u_form = CnPublicationUrlFormSet( instance=cnpublication)
      
    return render_to_response(template_name, {
        'form': form, 'f_form':f_form,'u_form': u_form,'issueform': issueform,  'commodityform': commodityform, "cnpublication": cnpublication
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
            
            f_form.instance = new_pfa
            f_form.save()
            
            u_form.instance = new_pfa
            u_form.save()
        
            
            info(request, _("Successfully created PestFreeArea."))
            
            return redirect("pfa-detail", country=user_country_slug, year=new_pfa.publish_date.strftime("%Y"), month=new_pfa.publish_date.strftime("%m"), slug=new_pfa.slug)
         else:
             return render_to_response('countries/pfa_create.html', {'form': form,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform},
             context_instance=RequestContext(request))
    else:
        form = PestFreeAreaForm(initial={'country': country}, instance=PestFreeArea())
        issueform =IssueKeywordsRelateForm(request.POST)
        commodityform =CommodityKeywordsRelateForm(request.POST)
        f_form =PestFreeAreaFileFormSet()
        u_form = PestFreeAreaUrlFormSet()

    return render_to_response('countries/pfa_create.html', {'form': form  ,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform},
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
        issues = get_object_or_404(IssueKeywordsRelate, pk=pfa.issuename.all()[0].id)
        commodities = get_object_or_404(CommodityKeywordsRelate, pk=pfa.commname.all()[0].id)
       
        # if pest_report.author != request.user:
        #     return HttpResponseForbidden()
    else:
        pfa = PestFreeArea(author=request.user)
      
    if request.POST:

        form = PestFreeAreaForm(request.POST,  request.FILES, instance=pfa)
        issueform =IssueKeywordsRelateForm(request.POST, instance=issues)
        commodityform =CommodityKeywordsRelateForm(request.POST, instance=commodities)
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
            
            f_form.instance = pfa
            f_form.save()
            u_form.instance = pfa
            u_form.save()
            # If the save was successful, success message and redirect to another page
            # info(request, _("Successfully updated pest report."))
            return redirect("pfa-detail", country=user_country_slug, year=pfa.publish_date.strftime("%Y"), month=pfa.publish_date.strftime("%m"), slug=pfa.slug)

    else:
        form = PestFreeAreaForm(instance=pfa)
        issueform =IssueKeywordsRelateForm(instance=issues)
        commodityform =CommodityKeywordsRelateForm(instance=commodities)
        f_form = PestFreeAreaFileFormSet(instance=pfa)
        u_form = PestFreeAreaUrlFormSet(instance=pfa)
        
    return render_to_response(template_name, {
        'form': form,'f_form':f_form,'u_form':u_form,'issueform': issueform,'commodityform': commodityform,  "pfa": pfa
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
            
            f_form.instance = new_implementationispm
            f_form.save()
            u_form.instance = new_implementationispm
            u_form.save()
            
            info(request, _("Successfully created implementationispm."))
            
            return redirect("implementationispm-detail", country=user_country_slug, year=new_implementationispm.publish_date.strftime("%Y"), month=new_implementationispm.publish_date.strftime("%m"), slug=new_implementationispm.slug)
        else:
             return render_to_response('countries/implementationispm_create.html', {'form': form,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform},
             context_instance=RequestContext(request))
    else:
        form = ImplementationISPMForm(initial={'country': country}, instance=ImplementationISPM())
        issueform =IssueKeywordsRelateForm(request.POST)
        commodityform =CommodityKeywordsRelateForm(request.POST)
        f_form =ImplementationISPMFileFormSet()
        u_form =ImplementationISPMUrlFormSet()

    return render_to_response('countries/implementationispm_create.html', {'form': form  ,'f_form': f_form,'u_form': u_form,'issueform':issueform, 'commodityform':commodityform},
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
        issues = get_object_or_404(IssueKeywordsRelate, pk=implementationispm.issuename.all()[0].id)
        commodities = get_object_or_404(CommodityKeywordsRelate, pk=implementationispm.commname.all()[0].id)
       
       # if pest_report.author != request.user:
        #     return HttpResponseForbidden()
    else:
        implementationispm = ImplementationISPM(author=request.user)
      
    if request.POST:
        form = ImplementationISPMForm(request.POST,  request.FILES, instance=implementationispm)
        issueform =IssueKeywordsRelateForm(request.POST, instance=issues)
        commodityform =CommodityKeywordsRelateForm(request.POST, instance=commodities)
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
            
            f_form.instance = implementationispm
            f_form.save()
            u_form.instance = implementationispm
            u_form.save()
            # If the save was successful, success message and redirect to another page
            # info(request, _("Successfully updated pest report."))
            return redirect("implementationispm-detail", country=user_country_slug, year=implementationispm.publish_date.strftime("%Y"), month=implementationispm.publish_date.strftime("%m"), slug=implementationispm.slug)

    else:
        form = ImplementationISPMForm(instance=implementationispm)
        issueform =IssueKeywordsRelateForm(instance=issues)
        commodityform =CommodityKeywordsRelateForm(instance=commodities)
        f_form = ImplementationISPMFileFormSet(instance=implementationispm)
        u_form = ImplementationISPMUrlFormSet(instance=implementationispm)
    return render_to_response(template_name, {
        'form': form,'f_form':f_form,'u_form': u_form,'issueform': issueform,'commodityform': commodityform,  "implementationispm": implementationispm
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
        issues = get_object_or_404(IssueKeywordsRelate, pk=countrynews.issuename.all()[0].id)
        commodities = get_object_or_404(CommodityKeywordsRelate, pk=countrynews.commname.all()[0].id)
       
       # if pest_report.author != request.user:
        #     return HttpResponseForbidden()
    else:
        countrynews = CountryNews(author=request.user)
      
    if request.POST:
        form = CountryNewsForm(request.POST,  request.FILES, instance=countrynews)
        issueform =IssueKeywordsRelateForm(request.POST, instance=issues)
        commodityform =CommodityKeywordsRelateForm(request.POST, instance=commodities)
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
        issueform =IssueKeywordsRelateForm(instance=issues)
        commodityform =CommodityKeywordsRelateForm(instance=commodities)
        f_form = CountryNewsFileFormSet(instance=countrynews)
        u_form = CountryNewsUrlFormSet(instance=countrynews)
    return render_to_response(template_name, {
        'form': form,'f_form':f_form,'u_form': u_form,'issueform': issueform,'commodityform': commodityform,  "countrynews": countrynews
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



class PollListView(ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'
    def get_queryset(self):
        """Return the last five published polls."""
        return Poll.objects.all


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
        print("-------")
        print(pollid)
        votes=PollVotes.objects.filter(poll_id=pollid)
        context['votes']= votes
        print(votes)
        return context
    
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

@login_required
@permission_required('ippc.add_emailutilitymessage', login_url="/accounts/login/")
def email_send(request):
    """ Create email to send """
    form = EmailUtilityMessageForm(request.POST)
  
    if request.method == "POST":
        f_form =EmailUtilityMessageFileFormSet(request.POST, request.FILES)
        if form.is_valid() and f_form.is_valid():
            emailto_all = [str(request.POST['emailto'])]
            for u in request.POST.getlist('users'):
                user_obj=User.objects.get(id=u)
                user_email=user_obj.email
                emailto_all.append(str(user_email))
            for g in request.POST.getlist('groups'):
                group=Group.objects.get(id=g)
                users = group.user_set.all()
                for u in users:
                   user_obj=User.objects.get(username=u)
                   user_email=user_obj.email
                   emailto_all.append(str(user_email))
            #save mail message in db
            new_emailmessage = form.save(commit=False)
            new_emailmessage.date=timezone.now()
            form.save()
            #save file to message in db
            f_form.instance = new_emailmessage
            f_form.save()
            #send email message
            message = mail.EmailMessage(request.POST['subject'],request.POST['messagebody'],request.POST['emailfrom'],
            emailto_all, ['paola.sentinelli@gmail.com'])
            # Attach a files to message
            fileset= EmailUtilityMessageFile.objects.filter(emailmessage_id=new_emailmessage.id)
            for f in fileset:
                pf='static/media/'+str(f.file)
                message.attach_file(pf) 
            sent =message.send()
            #update status mail message in db
            new_emailmessage.sent=sent
            form.save()
           
            info(request, _("Email  sent."))
            return redirect("email-detail",new_emailmessage.id)
        else:
             return render_to_response('emailutility/emailutility_send.html', {'form': form,'f_form': f_form},
             context_instance=RequestContext(request))
    else:
        form = EmailUtilityMessageForm(instance=EmailUtilityMessage())
        f_form =EmailUtilityMessageFileFormSet()
      
    return render_to_response('emailutility/emailutility_send.html', {'form': form  ,'f_form': f_form},
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
            for cn in cns:
              p=PestReport.objects.filter(country_id=cn.id).count()
              if p>0:
                maparray.append([str('<a href="'+cn.country_slug+'/pestreports/">'+cn.name)+': '+str(p)+'</a>',str(cn.cn_lat),str(cn.cn_long)])
            context['map']=maparray
            
                
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
        
        
        
        return context
		
		
		
	
