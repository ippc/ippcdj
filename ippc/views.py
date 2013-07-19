from django.shortcuts import render
from .models import IppcUserProfile, PestStatus, PestReport

from django.views.generic import ArchiveIndexView, MonthArchiveView, YearArchiveView, DetailView
from django.core.urlresolvers import reverse

# def latest_pest_reports(request):
#     pest_report_list = PestReport.objects.order_by('-publish_date')[:10]
#     return render(request, 'countries/pest_report_list.html', {'pest_report_list': pest_report_list})

# http://stackoverflow.com/questions/8547880/listing-object-with-specific-tag-using-django-taggit
# http://stackoverflow.com/a/7382708/412329
class PestReportListView(ArchiveIndexView):
    """
    Pest reports
    """
    context_object_name = 'latest'
    model = PestReport
    date_field = 'publish_date'
    template_name = 'countries/pest_report_list.html'
    queryset = PestReport.objects.all().order_by('-publish_date', 'title')
    allow_future = False

    # def get_dated_items(self):
    #     date_list, items, extra_context = super(PestReportListView, self).get_dated_items()
    #     return (date_list, items[:30], extra_context)

class PestReportDetailView(DetailView):
    """ Pest report permalink page """
    model = PestReport
    context_object_name = 'report'
    template_name = 'countries/pest_report_detail.html'