from django.shortcuts import render
from .models import IppcUserProfile, PestStatus, PestReport, PestReportForm

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
    allow_empty = True
    paginate_by = 2
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

# class PestReportCreateView(CreateView):
#     model = PestReport







# def manage_books(request, country_id):
#     country = Author.objects.get(pk=country_id)
#     BookInlineFormSet = inlineformset_factory(Author, Book)
#     if request.method == "POST":
#         formset = BookInlineFormSet(request.POST, request.FILES, instance=author)
#         if formset.is_valid():
#             formset.save()
#             # Do something. Should generally end with a redirect. For example:
#             return HttpResponseRedirect(author.get_absolute_url())
#     else:
#         formset = BookInlineFormSet(instance=author)
#     return render_to_response("manage_books.html", {
#         "formset": formset,
#     })






def pest_report_create(request):
    if request.method == "POST":

        form = form(request.POST, instance=PestReport())
        
        user = request.user
        # profile_user = request.profile_user
        author_id = user.id
        # country = request.user.get_profile.country
        
        if form.is_valid():
            new_pest_report = form.save(commit=False)
            new_pest_report.author_id = author_id
            # new_pest_report.country = country
            form.save()
            return HttpResponseRedirect('/countries/italy/pestreports/')
    else:
        form = form(instance=PestReport())
    return render_to_response('countries/pest_report_create.html', {'form': form},
        context_instance=RequestContext(request))




# @login_required
# def PestReportCreateView(request, country=None, template_name="countries/pest_report_create.html"):
# 
#     form = PestReportForm(request)
#     
#     if request.method == "POST" and form.is_valid():
#         pest_report = form.save(commit=False)
#         pest_report.author = request.user
#         
#         pest_report.country = 'Italy'
#         # pest_report.country = request.POST.country
#         form.save()
#         
#         pest_report.id = pest_report.id
#         pest_report.title = pest_report.title
#         pest_report.slug = slugify(pest_report.title)
#         # need to call save again so notification gets sent to observers 
#         # https://docs.djangoproject.com/en/dev/ref/models/instances/#saving-objects
#         
#         form.save()
#         # messages.add_message(request, messages.SUCCESS, message=_("Successfully created pest report '%s'") % pest_report.title)
#         # return redirect("pest-report-detail", country=pest_report.country.name, year=pest_report.publish_date.strftime("%Y"), month=pest_report.publish_date.strftime("%m"), slug=pest_report.slug)
#         return redirect("/countries/")
#     return render_to_response(template_name, {"form": form}, context_instance=RequestContext(request))



# http://stackoverflow.com/questions/907858/how-to-let-djangos-generic-view-use-a-form-with-initial-values