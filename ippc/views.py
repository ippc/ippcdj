from django.shortcuts import render
from .models import IppcUserProfile, PestStatus, PestReport
from .forms import PestReportForm

from django.views.generic import ArchiveIndexView, MonthArchiveView, YearArchiveView, DetailView, TemplateView, CreateView
from django.core.urlresolvers import reverse

from django.template.defaultfilters import slugify
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
    allow_empty = True
    paginate_by = 10
    queryset = PestReport.objects.all()
    
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




def get_profile():
    return IppcUserProfile.objects.all()

def pest_report_form_country():
    return IppcUserProfile.objects.filter(country=country)

# def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
#     context = super(pest_report_create, self).get_context_data(**kwargs)
#     context.update({
#         'country': self.kwargs['country']
#     })
#     return context






@login_required
@permission_required('ippc.add_pestreport', login_url="/accounts/login/")
def pest_report_create(request, country):

    user = request.user
    author = user
    # print('>>>>>>>>>>>>>>>')
    # print(user.get_profile().country)
    var1=user.get_profile().country

    form = PestReportForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            new_pest_report = form.save(commit=False)
            new_pest_report.author = request.user
            new_pest_report.author_id = author.id
            form.save()
            return redirect("pest-report-detail", country=country, year=new_pest_report.publish_date.strftime("%Y"), month=new_pest_report.publish_date.strftime("%m"), slug=new_pest_report.slug)
    else:

        form = PestReportForm(initial={'country': var1}, instance=PestReport())

    return render_to_response('countries/pest_report_create.html', {'form': form},
        context_instance=RequestContext(request))


@login_required
@permission_required('ippc.change_pestreport', login_url="/accounts/login/")
def pest_report_edit(request, id, form_class=PestReportForm, template_name="countries/pest_report_edit.html"):
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
        return redirect("pest-report-detail", username=request.user.username, slug=pest_report.slug)
    return render_to_response(template_name, {"pest_report_form": pest_report_form, "pest_report": pest_report}, context_instance=RequestContext(request))








# @login_required
# def PestReportCreateView(request, country=None, template_name="countries/pest_report_create.html"):
# 
#     form = PestReportForm(request)
#     
#     if request.method == "POST" and form.is_valid():
#         pest_report = form.save(commit=False)
#         pest_report.author = request.user
#         # profile = IppcUserProfile.objects.all()
#         country = country
#         # pest_report.id = pest_report.id
#         pest_report.title = pest_report.title
#         pest_report.slug = slugify(pest_report.title)
#         # need to call save again so notification gets sent to observers 
#         # https://docs.djangoproject.com/en/dev/ref/models/instances/#saving-objects
#         
#         form.save()
#         # messages.add_message(request, messages.SUCCESS, message=_("Successfully created pest report '%s'") % pest_report.title)
#         # return redirect("pest-report-detail", country=pest_report.country.name, year=pest_report.publish_date.strftime("%Y"), month=pest_report.publish_date.strftime("%m"), slug=pest_report.slug)
#         
#         return redirect("/countries/")
#     return render_to_response(template_name, {"form": form}, context_instance=RequestContext(request))



# http://stackoverflow.com/questions/907858/how-to-let-djangos-generic-view-use-a-form-with-initial-values