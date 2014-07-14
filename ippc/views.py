from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages import info, error
from .models import IppcUserProfile, PestStatus, PestReport, IS_PUBLIC, IS_HIDDEN, Publication, ReportingObligation, BASIC_REP_TYPE_CHOICES, EventReporting, EVT_REP_TYPE_CHOICES,PestFreeArea,ImplementationISPM, ForumPost
from mezzanine.core.models import Displayable, CONTENT_STATUS_DRAFT, CONTENT_STATUS_PUBLISHED
from .forms import PestReportForm, ReportingObligationForm, EventReportingForm, PestFreeAreaForm,ImplementationISPMForm

from django.views.generic import ListView, MonthArchiveView, YearArchiveView, DetailView, TemplateView, CreateView
from django.core.urlresolvers import reverse

from django.template.defaultfilters import slugify, lower
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

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
    # print('>>>>>>>>>>>>>>>')
    # print(user.get_profile().country)

class ForumPostDetailView(DetailView):
    """ Forum post detail page """
    model = ForumPost
    context_object_name = 'post'
    template_name = 'forum/forum_post_detail.html'
    # queryset = PestReport.objects.filter(status=CONTENT_STATUS_PUBLISHED)
    # print('>>>>>>>>>>>>>>>')
    # print(user.get_profile().country)


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
    
    if request.method == "POST":
        if form.is_valid():
            new_pest_report = form.save(commit=False)
            new_pest_report.author = request.user
            new_pest_report.author_id = author.id
            form.save()
            info(request, _("Successfully created pest report."))
            
            if new_pest_report.status == CONTENT_STATUS_DRAFT:
                return redirect("pest-report-hidden-list", country=user_country_slug)
            else:
                return redirect("pest-report-detail", country=user_country_slug, year=new_pest_report.publish_date.strftime("%Y"), month=new_pest_report.publish_date.strftime("%m"), slug=new_pest_report.slug)
    else:

        form = PestReportForm(initial={'country': country}, instance=PestReport())
    
    return render_to_response('countries/pest_report_create.html', {'form': form},
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
        # if pest_report.author != request.user:
        #     return HttpResponseForbidden()
    else:
        pest_report = PestReport(author=request.user)

    if request.POST:
        form = PestReportForm(request.POST, request.FILES, instance=pest_report)

        if form.is_valid():
            form.save()

            # If the save was successful, success message and redirect to another page
            # info(request, _("Successfully updated pest report."))
            if pest_report.status == CONTENT_STATUS_DRAFT:
                return redirect("pest-report-hidden-list", country=user_country_slug)
            else:
                return redirect("pest-report-detail", country=user_country_slug, year=pest_report.publish_date.strftime("%Y"), month=pest_report.publish_date.strftime("%m"), slug=pest_report.slug)

    else:
        form = PestReportForm(instance=pest_report)

    return render_to_response(template_name, {
        'form': form, "pest_report": pest_report
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
    # print('>>>>>>>>>>>>>>>')
    # print(user.get_profile().country)



@login_required
@permission_required('ippc.add_reportingobligation', login_url="/accounts/login/")
def reporting_obligation_create(request, country,type):
    """ Create Reporting Obligation """
    user = request.user
    author = user
    country=user.get_profile().country
    user_country_slug = lower(slugify(country))

    form = ReportingObligationForm(request.POST, request.FILES)
  
    if request.method == "POST":
        if form.is_valid():
            new_reporting_obligation = form.save(commit=False)
            new_reporting_obligation.author = request.user
            new_reporting_obligation.author_id = author.id
            new_reporting_obligation.report_obligation_type = type
            form.save()
            info(request, _("Successfully created reporting_obligation."))
            
            return redirect("basic-reporting-detail", country=user_country_slug, year=new_reporting_obligation.publish_date.strftime("%Y"), month=new_reporting_obligation.publish_date.strftime("%m"), slug=new_reporting_obligation.slug)
    else:
        form = ReportingObligationForm(initial={'country': country,'report_obligation_type': type}, instance=ReportingObligation())
    
    return render_to_response('countries/reporting_obligation_create.html', {'form': form},
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
        # if pest_report.author != request.user:
        #     return HttpResponseForbidden()
    else:
        reporting_obligation = ReportingObligation(author=request.user)
      
    if request.POST:
        form = ReportingObligationForm(request.POST, request.FILES, instance=reporting_obligation)
        if form.is_valid():
            form.save()

            # If the save was successful, success message and redirect to another page
            # info(request, _("Successfully updated pest report."))
            return redirect("basic-reporting-detail", country=user_country_slug, year=reporting_obligation.publish_date.strftime("%Y"), month=reporting_obligation.publish_date.strftime("%m"), slug=reporting_obligation.slug)

    else:
        form = ReportingObligationForm(instance=reporting_obligation)

    return render_to_response(template_name, {
        'form': form, "reporting_obligation": reporting_obligation
    }, context_instance=RequestContext(request))
    


class EventReportingListView(ListView):
    """    Event Reporting """
    context_object_name = 'latest'
    model = ReportingObligation
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
    # print('>>>>>>>>>>>>>>>')
    # print(user.get_profile().country)



@login_required
@permission_required('ippc.add_eventreporting', login_url="/accounts/login/")
def event_reporting_create(request, country,type):
    """ Create Event Reporting """
    user = request.user
    author = user
    country=user.get_profile().country
    user_country_slug = lower(slugify(country))

    form = EventReportingForm(request.POST, request.FILES)
  
    if request.method == "POST":
        if form.is_valid():
            new_event_reporting = form.save(commit=False)
            new_event_reporting.author = request.user
            new_event_reporting.author_id = author.id
            new_event_reporting.event_rep_type = type
            form.save()
            info(request, _("Successfully created event reporting."))
            
            return redirect("event-reporting-detail", country=user_country_slug, year=new_event_reporting.publish_date.strftime("%Y"), month=new_event_reporting.publish_date.strftime("%m"), slug=new_event_reporting.slug)
    else:
        form = EventReportingForm(initial={'country': country,'event_rep_type': type}, instance=EventReporting())
    
    return render_to_response('countries/event_reporting_create.html', {'form': form},
        context_instance=RequestContext(request))

        
# http://stackoverflow.com/a/1854453/412329
@login_required
@permission_required('ippc.change_eventreporting', login_url="/accounts/login/")
def event_reporting_edit(request, country, id=None, template_name='countries/event_reporting_edit.html'):
    """ Edit Reporting Obligation """
    user = request.user
    author = user
    country = user.get_profile().country
    # country_id = PestReport.objects.filter(country__country_id=country.id)
    user_country_slug = lower(slugify(country))
    if id:
        event_reporting = get_object_or_404(EventReporting, country=country, pk=id)
        # if pest_report.author != request.user:
        #     return HttpResponseForbidden()
    else:
        event_reporting = EventReporting(author=request.user)
      
    if request.POST:
        form = EventReportingForm(request.POST, request.FILES, instance=event_reporting)
        if form.is_valid():
            form.save()

            # If the save was successful, success message and redirect to another page
            # info(request, _("Successfully updated pest report."))
            return redirect("event-reporting-detail", country=user_country_slug, year=event_reporting.publish_date.strftime("%Y"), month=event_reporting.publish_date.strftime("%m"), slug=event_reporting.slug)

    else:
        form = EventReportingForm(instance=event_reporting)

    return render_to_response(template_name, {
        'form': form, "event_reporting": event_reporting
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
    # print('>>>>>>>>>>>>>>>')
    # print(user.get_profile().country)



@login_required
@permission_required('ippc.add_pestfreearea', login_url="/accounts/login/")
def pfa_create(request, country):
    """ Create PestFreeArea """
    user = request.user
    author = user
    country=user.get_profile().country
    user_country_slug = lower(slugify(country))

    form = PestFreeAreaForm(request.POST, request.FILES)
  
    if request.method == "POST":
        if form.is_valid():
            new_pfa = form.save(commit=False)
            new_pfa.author = request.user
            new_pfa.author_id = author.id
            form.save()
            info(request, _("Successfully created PestFreeArea."))
            
            return redirect("pfa-detail", country=user_country_slug, year=new_pfa.publish_date.strftime("%Y"), month=new_pfa.publish_date.strftime("%m"), slug=new_pfa.slug)
    else:
        form = PestFreeAreaForm(initial={'country': country}, instance=PestFreeArea())
    
    return render_to_response('countries/pfa_create.html', {'form': form},
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
        # if pest_report.author != request.user:
        #     return HttpResponseForbidden()
    else:
        pfa = PestFreeArea(author=request.user)
      
    if request.POST:
        form = PestFreeAreaForm(request.POST, request.FILES, instance=pfa)
        if form.is_valid():
            form.save()

            # If the save was successful, success message and redirect to another page
            # info(request, _("Successfully updated pest report."))
            return redirect("pfa-detail", country=user_country_slug, year=pfa.publish_date.strftime("%Y"), month=pfa.publish_date.strftime("%m"), slug=pfa.slug)

    else:
        form = PestFreeAreaForm(instance=pfa)

    return render_to_response(template_name, {
        'form': form, "pfa": pfa
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
    # print('>>>>>>>>>>>>>>>')
    # print(user.get_profile().country)



@login_required
@permission_required('ippc.add_implementationispm', login_url="/accounts/login/")
def implementationispm_create(request, country):
    """ Create ImplementationISPM """
    user = request.user
    author = user
    country=user.get_profile().country
    user_country_slug = lower(slugify(country))

    form = ImplementationISPMForm(request.POST, request.FILES)
  
    if request.method == "POST":
        if form.is_valid():
            new_implementationispm = form.save(commit=False)
            new_implementationispm.author = request.user
            new_implementationispm.author_id = author.id
            form.save()
            info(request, _("Successfully created implementationispm."))
            
            return redirect("implementationispm-detail", country=user_country_slug, year=new_implementationispm.publish_date.strftime("%Y"), month=new_implementationispm.publish_date.strftime("%m"), slug=new_implementationispm.slug)
    else:
        form = ImplementationISPMForm(initial={'country': country}, instance=ImplementationISPM())
    
    return render_to_response('countries/implementationispm_create.html', {'form': form},
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
        # if pest_report.author != request.user:
        #     return HttpResponseForbidden()
    else:
        implementationispm = ImplementationISPM(author=request.user)
      
    if request.POST:
        form = ImplementationISPMForm(request.POST, request.FILES, instance=implementationispm)
        if form.is_valid():
            form.save()

            # If the save was successful, success message and redirect to another page
            # info(request, _("Successfully updated pest report."))
            return redirect("implementationispm-detail", country=user_country_slug, year=implementationispm.publish_date.strftime("%Y"), month=implementationispm.publish_date.strftime("%m"), slug=implementationispm.slug)

    else:
        form = ImplementationISPMForm(instance=implementationispm)

    return render_to_response(template_name, {
        'form': form, "implementationispm": implementationispm
    }, context_instance=RequestContext(request))
    
