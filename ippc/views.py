from django.shortcuts import render
from .models import IppcUserProfile, PestStatus, PestReport
from .forms import PestReportForm

from django.views.generic import ListView, MonthArchiveView, YearArchiveView, DetailView, TemplateView, CreateView
from django.core.urlresolvers import reverse

from django.template.defaultfilters import slugify, lower
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required, permission_required

# from mezzanine.utils.models import get_user_model
# User = get_user_model()
# 
# def country_view(request, country, template="countries/country_page.html"):
#     """
#     Display a country homepage with user info.
#     """
#     country = {"country__iexact": country}
#     context = {"user": get_object_or_404(User, **country)}
#     return render(request, country, template, context)

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
        context.update({
            'country': self.kwargs['country']
            # 'editors': self.kwargs['editors']
            # 'profile_user': self.kwargs['profile_user']
        })
        return context


from django_countries.fields import Country
from django.db.models import F

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
        return PestReport.objects.filter(country__country_slug=self.country)
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(PestReportListView, self).get_context_data(**kwargs)
        context['country'] = self.kwargs['country']
        # context.update({
        #     'country': self.kwargs['country']
        # })
        return context

class PestReportDetailView(DetailView):
    """ Pest report detail page """
    model = PestReport
    context_object_name = 'report'
    template_name = 'countries/pest_report_detail.html'
    # print('>>>>>>>>>>>>>>>')
    # print(user.get_profile().country)

@login_required
@permission_required('ippc.add_pestreport', login_url="/accounts/login/")
def pest_report_create(request, country):
    """ Create Pest Report """
    user = request.user
    author = user
    country=user.get_profile().country
    user_country_slug = lower(slugify(country))

    form = PestReportForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            new_pest_report = form.save(commit=False)
            new_pest_report.author = request.user
            new_pest_report.author_id = author.id
            form.save()
            return redirect("pest-report-detail", country=user_country_slug, year=new_pest_report.publish_date.strftime("%Y"), month=new_pest_report.publish_date.strftime("%m"), slug=new_pest_report.slug)
    else:

        form = PestReportForm(initial={'country': country}, instance=PestReport())

    return render_to_response('countries/pest_report_create.html', {'form': form},
        context_instance=RequestContext(request))

@login_required
@permission_required('ippc.change_pestreport', login_url="/accounts/login/")
def pest_report_edit(request, country, id, form_class=PestReportForm, template_name="countries/pest_report_edit.html"):
    """ Edit Pest Report """
    user = request.user
    author = user
    country=user.get_profile().country
    user_country_slug = lower(slugify(country))
    pest_report = get_object_or_404(PestReport, id=id)
    # if pest_report.author != request.user:
    #     request.user.message_set.create(message="You can't edit items that aren't yours")
    #     return redirect("/")
    pest_report_form = form_class(request, instance=pest_report)
    if request.method == "POST" and pest_report_form.is_valid():
        pest_report = pest_report_form.save(commit=False)
        pest_report.modify_date = datetime.now()
        pest_report_form.save()
        # request.user.message_set.create(message=_("Successfully updated pest_report '%s'") % pest_report.title)
        # http://stackoverflow.com/a/11728475/412329
        # messages.add_message(request, messages.SUCCESS, message=_("Successfully updated pest_report '%s'") % pest_report.title)
        return redirect("pest-report-detail", country=user_country_slug, year=new_pest_report.publish_date.strftime("%Y"), month=new_pest_report.publish_date.strftime("%m"), slug=new_pest_report.slug)
    return render_to_response(template_name, {"pest_report_form": pest_report_form, "pest_report": pest_report}, context_instance=RequestContext(request))