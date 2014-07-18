# -*- coding: utf-8 -*-

from django import forms
import datetime
from .models import IppcUserProfile, PestStatus, PestReport,  CountryPage, \
ReportingObligation, EventReporting, PestFreeArea, ImplementationISPM, Website, \
VERS_CHOICES,IssueKeywordsRelate,CommodityKeywordsRelate,\
EventreportingFile, ReportingObligation_File,PestFreeAreaFile, ImplementationISPMFile,PestReportFile,\
EventreportingUrl, ReportingObligationUrl,PestFreeAreaUrl, ImplementationISPMUrl,PestReportUrl,WebsiteUrl,\
CnPublication,CnPublicationFile,CnPublicationUrl

from django.contrib.auth.models import User
import autocomplete_light
import autocomplete_light_registry
from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory
from django.contrib.admin.widgets import AdminDateWidget 

class PestReportForm(forms.ModelForm):

    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values

    class Meta:
        model = PestReport
        fields = [
            'country',
            'title', 
            'summary',
            # 'is_public',
            'status',
            # 'slug', 
            # 'publish_date', 
            'report_status', 
            'pest_status',
            'pest_identity',
            'hosts',
            'geographical_distribution',
            'nature_of_danger',
            'contact_for_more_information',
            ]
        exclude = ('author', 'slug', 'publish_date', 'modify_date' )
        widgets = {
            'country': forms.HiddenInput(),
            'report_number': forms.HiddenInput(),
            'pest_identity': autocomplete_light.ChoiceWidget ('EppoCodeAutocomplete'),
        }


class IssueKeywordsRelateForm(forms.ModelForm):
    class Meta:
        model =  IssueKeywordsRelate
        fields = [
            'issuename',]
        widgets = {
         'issuename': autocomplete_light.MultipleChoiceWidget ('IssueKeywordAutocomplete'),   
         }
class CommodityKeywordsRelateForm(forms.ModelForm):
    class Meta:
        model =  CommodityKeywordsRelate
        fields = [
            'commname',]
        widgets = {
         'commname': autocomplete_light.MultipleChoiceWidget ('CommodityKeywordAutocomplete'),   
         }   


class IssueKeywordsRelateForm(forms.ModelForm):
    class Meta:
        model =  IssueKeywordsRelate
        fields = [
            'issuename',]
        widgets = {
         'issuename': autocomplete_light.MultipleChoiceWidget ('IssueKeywordAutocomplete'),   
         }


class ReportingObligationForm(forms.ModelForm):

    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values

    class Meta:
        model = ReportingObligation
        fields = [

           'reporting_obligation_type',
           'title', 
           'publication_date', 
           'short_description',
           'contact_for_more_information',
           'country',
           ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date')
        widgets = {
            'country': forms.HiddenInput(),   
            'reporting_obligation_type': forms.RadioSelect(attrs={'readonly':'True'}),
            'publication_date': AdminDateWidget(),
      }

class EventReportingForm(forms.ModelForm):
   # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values
   
    class Meta:
        model = EventReporting
        fields = [
           'event_rep_type',
           'title', 
           'publication_date', 
           'short_description',
           'contact_for_more_information',
           'country',
            ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date',  'old_id')
        widgets = {
            'country': forms.HiddenInput(),   
            'event_rep_type': forms.RadioSelect(attrs={'readonly':'True'}),
            'publication_date': AdminDateWidget(),
          }
 
  
class PestFreeAreaForm(forms.ModelForm):
   # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values
    class Meta:
        model = PestFreeArea
        fields = [
           'title', 
           'short_description',
           'publication_date', 
           'pfa_type',
           'contact_for_more_information',
           'country',
           ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date')
        widgets = {
            'country': forms.HiddenInput(),
             'publication_date': AdminDateWidget(),
        }
       
class ImplementationISPMForm(forms.ModelForm):
    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values
    class Meta:
        model = ImplementationISPM
        fields = [
           'title', 
           'publication_date', 
           'implementimport_type',
           'implementimport_version',
           'implementexport_type',
           'implementexport_version',
           'mark_registered_type',
           'image',
           'short_description',
           'contact_for_more_information',
           'country',
           ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date')
        widgets = {
            'country': forms.HiddenInput(),
            'implementimport_type':forms.RadioSelect(),
            'implementexport_type':forms.RadioSelect(),
            'publication_date': AdminDateWidget(),
           }
           
class WebsiteForm(forms.ModelForm):
   # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values
   
    class Meta:
        model = Website
        fields = [
            'title', 
            'short_description',
            'web_type',
            'contact_for_more_information',
            'country',
            ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date',  'old_id')
        widgets = {
            'country': forms.HiddenInput(),   
          }

class CnPublicationForm(forms.ModelForm):

    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values

    class Meta:
        model = CnPublication
        fields = [
           'title', 
           'publication_date', 
           'agenda_number',
           'document_number',
            'short_description',
           'contact_for_more_information',
           'country',
           ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date')
        widgets = {
            'country': forms.HiddenInput(),   
            'publication_date': AdminDateWidget(),
        }

CnPublicationUrlFormSet  = inlineformset_factory(CnPublication,  CnPublicationUrl, extra=1)
CnPublicationFileFormSet = inlineformset_factory(CnPublication,  CnPublicationFile,extra=1)
       
        
        
        
WebsiteUrlFormSet  = inlineformset_factory(Website,  WebsiteUrl, extra=1)

EventreportingUrlFormSet  = inlineformset_factory(EventReporting,  EventreportingUrl, extra=1)
EventreportingFileFormSet = inlineformset_factory(EventReporting,  EventreportingFile,extra=1)


ImplementationISPMFileFormSet = inlineformset_factory(ImplementationISPM,  ImplementationISPMFile,extra=1)
ImplementationISPMUrlFormSet  = inlineformset_factory(ImplementationISPM,  ImplementationISPMUrl, extra=1)

PestFreeAreaFileFormSet = inlineformset_factory(PestFreeArea,  PestFreeAreaFile,extra=1) 
PestFreeAreaUrlFormSet  = inlineformset_factory(PestFreeArea,  PestFreeAreaUrl, extra=1)

PestReportFileFormSet = inlineformset_factory(PestReport,  PestReportFile,extra=1)
PestReportUrlFormSet  = inlineformset_factory(PestReport,  PestReportUrl, extra=1)

ReportingoblicationFileFormSet = inlineformset_factory(ReportingObligation,  ReportingObligation_File,extra=1)
ReportingObligationUrlFormSet  = inlineformset_factory(ReportingObligation,  ReportingObligationUrl, extra=1)

  
