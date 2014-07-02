# -*- coding: utf-8 -*-

from django import forms
from .models import IppcUserProfile, PestStatus, PestReport,  CountryPage, \
ReportingObligation, EventReporting, PestFreeArea, ImplementationISPM, \
VERS_CHOICES,IssueKeywordsRelate,CommodityKeywordsRelate,EventreportingFile
from django.contrib.auth.models import User
import autocomplete_light
import autocomplete_light_registry
from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory

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
            'file',
            'pest_status',
            'pest_identity',
            'hosts',
            'geographical_distribution',
            'nature_of_danger',
            'contact_for_more_information',
            'url_for_more_information',
            ]
        exclude = ('author', 'slug', 'publish_date', 'modify_date')
        widgets = {
            'country': forms.HiddenInput(),
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

class ReportingObligationForm(forms.ModelForm):

    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values

    class Meta:
        model = ReportingObligation
        fields = [
           'reporting_obligation_type',
           'title', 
           'publication_date', 
           'file',
           'short_description',
           'contact_for_more_information',
           'url_for_more_information',
           'country',
          
           ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date')
        widgets = {
            'country': forms.HiddenInput(),   
            'reporting_obligation_type': forms.RadioSelect(attrs={'readonly':'True'}),
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
          # 'file',
           'short_description',
           'contact_for_more_information',
           'url_for_more_information',
           'country',
            ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date')
        widgets = {
            'country': forms.HiddenInput(),   
            'event_rep_type': forms.RadioSelect(attrs={'readonly':'True'}),
          }
 
EventreportingFileFormSet = inlineformset_factory(EventReporting,  EventreportingFile,extra=1)
    
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
           'file',
           'contact_for_more_information',
           'url_for_more_information',
           'country',
         
            ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date')
        widgets = {
            'country': forms.HiddenInput(),
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
           'file',
           'mark_registered_type',
           'image',
           'short_description',
           'contact_for_more_information',
           'url_for_more_information',
           'country',
           ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date')
        widgets = {
            'country': forms.HiddenInput(),
            'implementimport_type':forms.RadioSelect(),
            'implementexport_type':forms.RadioSelect(),
           }