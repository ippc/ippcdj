from django.shortcuts import render
from .models import IppcUserProfile, PestStatus, PestReport
from .forms import PestReportForm

from django.views.generic import ArchiveIndexView, MonthArchiveView, YearArchiveView, DetailView, TemplateView, CreateView
from django.core.urlresolvers import reverse

from django.template.defaultfilters import slugify
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required

class CountryView(TemplateView):
    """ 
    Individual country homepage 
    """
    template_name = 'countries/country_page.html'

class PestReportListView(ArchiveIndexView):
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
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(PestReportListView, self).get_context_data(**kwargs)
        context.update({
            'country': self.kwargs['country']
        })
        return context

class PestReportDetailView(DetailView):
    """ 
    Pest report permalink page 
    """
    model = PestReport
    context_object_name = 'report'
    template_name = 'countries/pest_report_detail.html'

# class PestReportCreateView(CreateView):
#     model = PestReport

# @login_required
def PestReportCreateView(request, country, form_class=PestReportForm, template_name="countries/pest_report_add.html"):
    # u = request.GET.get('u', '')
    # t = request.GET.get('t', '')
    country = request.GET.get('country', '')
    pest_report_form = form_class(request)
    if request.method == "POST" and pest_report_form.is_valid():
        pest_report = pest_report_form.save(commit=False)
        pest_report.author = request.user
        pest_report.country = request.user.get_profile.country
        pest_report_form.save()
        # pest_report.country = profile_user.get_profile.country.name
        pest_report.id = pest_report.id
        pest_report.title = pest_report.title
        pest_report.slug = slugify(pest_report.title)
        # need to call save again so notification gets sent to observers 
        # https://docs.djangoproject.com/en/dev/ref/models/instances/#saving-objects
        pest_report_form.save()
        # messages.add_message(request, messages.SUCCESS, message=_("Successfully created pest report '%s'") % pest_report.title)
        # return redirect("pest-report-detail", country=pest_report.country.name, year=pest_report.publish_date.strftime("%Y"), month=pest_report.publish_date.strftime("%m"), slug=pest_report.slug)
        return redirect("/countries/")
    return render_to_response(template_name, {"pest_report_form": pest_report_form}, context_instance=RequestContext(request))



# http://stackoverflow.com/questions/907858/how-to-let-djangos-generic-view-use-a-form-with-initial-values