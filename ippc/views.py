from django.shortcuts import render
from .models import IppcUserProfile, CountryPage, PestStatus, PestReport

def latest_pest_reports(request):
    pest_report_list = PestReport.objects.order_by('-publish_date')[:10]
    return render(request, 'countries/pest_report_list.html', {'pest_report_list': pest_report_list})