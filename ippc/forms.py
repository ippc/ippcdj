# -*- coding: utf-8 -*-

from django import forms
import datetime
from .models import Publication,PublicationFile,PublicationUrl, IppcUserProfile, PestStatus, PestReport,  CountryPage, \
ReportingObligation, EventReporting, PestFreeArea, ImplementationISPM, Website, \
VERS_CHOICES,IssueKeywordsRelate,CommodityKeywordsRelate,\
EventreportingFile, ReportingObligation_File,PestFreeAreaFile, ImplementationISPMFile,PestReportFile,\
EventreportingUrl, ReportingObligationUrl,PestFreeAreaUrl, ImplementationISPMUrl,PestReportUrl,WebsiteUrl,\
CnPublication,CnPublicationFile,CnPublicationUrl,\
PartnersWebsite,PartnersWebsiteUrl,\
PartnersPublication,PartnersPublicationFile,PartnersPublicationUrl,\
PartnersNews,PartnersNewsFile,PartnersNewsUrl, \
CountryNews,CountryNewsFile,CountryNewsUrl, EmailUtilityMessage, EmailUtilityMessageFile

from django.contrib.auth.models import User,Group
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
class PartnersWebsiteForm(forms.ModelForm):
   # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values
   
    class Meta:
        model =  PartnersWebsite
        fields = [
            'title', 
            'short_description',
            'web_type',
            'contact_for_more_information',
            'partners',
            ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date',  'old_id')
        widgets = {
            'partners': forms.HiddenInput(),   
          }
          
class PublicationForm(forms.ModelForm):

    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values

    class Meta:
        model = Publication
        fields = [
           'title', 
           'library', 
           'file_en',
           'file_es',
           'file_fr',
           'file_ar',
           'file_ru',
           'file_zh',
           'agenda_number',
           'document_number',
           'short_description',
           'contact_for_more_information',
           ]
        exclude = ('author', 'slug', 'modify_date')
      
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
class PartnersPublicationForm(forms.ModelForm):

    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values

    class Meta:
        model = PartnersPublication
        fields = [
           'title', 
           'publication_date', 
           'agenda_number',
           'document_number',
            'short_description',
           'contact_for_more_information',
           'partners',
           ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date')
        widgets = {
            'partners': forms.HiddenInput(),   
            'publication_date': AdminDateWidget(),
        }        
class CountryNewsForm(forms.ModelForm):
    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values
    class Meta:
        model = CountryNews
        fields = [
           'title', 
           'publication_date', 
           'short_description',
           'image',
           'contact_for_more_information',
           'country',
           ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date')
        widgets = {
            'country': forms.HiddenInput(),
            'publication_date': AdminDateWidget(),
           }
class PartnersNewsForm(forms.ModelForm):
    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values
    class Meta:
        model = PartnersNews
        fields = [
           'title', 
           'publication_date', 
           'short_description',
           'image',
           'contact_for_more_information',
           'partners',
           ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date')
        widgets = {
            'partners': forms.HiddenInput(),
            'publication_date': AdminDateWidget(),
           }
           
PublicationUrlFormSet  = inlineformset_factory(Publication,  PublicationUrl, extra=1)
PublicationFileFormSet = inlineformset_factory(Publication,  PublicationFile,extra=1)
                 
CountryNewsUrlFormSet  = inlineformset_factory(CountryNews,  CountryNewsUrl, extra=1)
CountryNewsFileFormSet = inlineformset_factory(CountryNews,  CountryNewsFile,extra=1)
PartnersNewsUrlFormSet  = inlineformset_factory(PartnersNews,  PartnersNewsUrl, extra=1)
PartnersNewsFileFormSet = inlineformset_factory(PartnersNews,  PartnersNewsFile,extra=1)
                  
CnPublicationUrlFormSet  = inlineformset_factory(CnPublication,  CnPublicationUrl, extra=1)
CnPublicationFileFormSet = inlineformset_factory(CnPublication,  CnPublicationFile,extra=1)
       
PartnersPublicationUrlFormSet  = inlineformset_factory(PartnersPublication,  PartnersPublicationUrl, extra=1)
PartnersPublicationFileFormSet = inlineformset_factory(PartnersPublication,  PartnersPublicationFile,extra=1)
       
               
        
        
WebsiteUrlFormSet  = inlineformset_factory(Website,  WebsiteUrl, extra=1)
PartnersWebsiteUrlFormSet  = inlineformset_factory(PartnersWebsite,  PartnersWebsiteUrl, extra=1)
 
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



class EmailUtilityMessageForm(forms.ModelForm):

    class Meta:
        model = EmailUtilityMessage
        fields = [
           'emailfrom',
           'subject', 
           'messagebody',
           'emailto',
           'users',
           ]
       
        exclude = ( 'date','sent', 'groups',)
       
#        widgets = {
#            'groups': forms.CheckboxSelectMultiple()
#     }  
     
#  
EmailUtilityMessageFileFormSet = inlineformset_factory(EmailUtilityMessage,  EmailUtilityMessageFile,extra=1)

    