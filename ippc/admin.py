# https://gist.github.com/renyi/3596248
from copy import deepcopy
from django.contrib import admin
from mezzanine.pages.models import Page, RichTextPage, Link
from mezzanine.pages.admin import PageAdmin, LinkAdmin
from mezzanine.conf import settings
from mezzanine.core.admin import TabularDynamicInlineAdmin, StackedDynamicInlineAdmin,DisplayableAdmin, OwnableAdmin
from settings import ALLOWED_HOSTS 

from .models import DraftProtocol,PartnersEditorHistory, PartnersContactPointHistory, OCPHistory,CnEditorsHistory,PestStatus, PestReport, CountryPage, PartnersPage, WorkAreaPage, PublicationLibrary, \
Publication,PublicationFile,PublicationUrl, ReportingObligation,EventReporting,PestFreeArea,ImplementationISPM, Poll_Choice, Poll,\
ImplementationISPMVersion, TransPublicationLibraryPage,Website,EventreportingFile,EventreportingUrl,\
ReportingObligation_File, ReportingObligationUrl,ImplementationISPMUrl,ImplementationISPMFile,\
PestFreeAreaFile, PestFreeAreaUrl, WebsiteUrl,PestReportUrl,PestReportFile,CnPublication,CnPublicationFile,CnPublicationUrl,PartnersPublication,PartnersPublicationFile,PartnersPublicationUrl, \
CountryNews,CountryNewsFile,CountryNewsUrl,CommodityKeyword,PreferredLanguages,  \
PartnersWebsite,PartnersWebsiteUrl,\
PartnersNews,PartnersNewsFile,PartnersNewsUrl, \
EppoCode,IssueKeyword, CommodityKeyword,IssueKeywordsRelate,CommodityKeywordsRelate, ContactType, IppcUserProfile,\
QAQuestion,QAAnswer,FAQsCategory,FAQsItem,IRSSActivity,IRSSActivityFile,TransFAQsCategory,TransFAQsItem,UserMembershipHistory
#,TransReportingObligation

from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory
from django.contrib.auth.models import User,Group
from django import forms
from django.core import mail
from django.core.mail import send_mail
from models import TransRichTextPage, TransLinkPage
from django_markdown.admin import MarkdownModelAdmin

from django.shortcuts import get_object_or_404

import autocomplete_light
#import autocomplete_light_registry

from django_markdown.widgets import MarkdownWidget

# for login as user
class IppcUserProfileAdmin(admin.ModelAdmin):
    change_form_template = 'loginas/change_form.html'
 
class MyQAQuestionAdminForm(forms.ModelForm):
    class Meta:
        model = QAQuestion
        widgets = { 'short_description':MarkdownWidget() 
#         # models.TextField: {'widget': },
}
class QAQuestionAdmin(admin.ModelAdmin):
    form = MyQAQuestionAdminForm
    fieldsets = [
        ('Title',{'fields': ['title'], 'classes': ['nocollapse']}),
        ('Description',{'fields': ['short_description'], 'classes': ['Textarea']}),
        ('publish_date', {'fields': ['publish_date'], 'classes': ['nocollapse']}),
        ('Author', {'fields': ['user'], 'classes': ['nocollapse']}),
        ('Open', {'fields': ['questionopen'], 'classes': ['nocollapse']}),
        ('Status', {'fields': ['status'], 'classes': ['nocollapse']}),
        ('Publish or Reject question', {'fields': ['questiondiscard'], 'classes': ['collapse']}),
    ]
    list_display = ('title','short_description', 'publish_date','status','questionopen','user','questiondiscard')
    search_fields = ['short_description']
    list_filter = ['publish_date','short_description','status']

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        admin.ModelAdmin.save_form(self, request, form, change)
        if request.POST['questiondiscard']!=None:
            if request.POST['questiondiscard'] == '2':  
                emailto_all = []
                user_obj=User.objects.get(id= request.POST['user'])
                emailto_all.append(str(user_obj.email))
                subject='IRSS - Q&A Forum automatic notification: your question has been published.'    
                textmessage='<html><body><p>Dear IPPC user,<br><br>Your question has been reviewed and now has been published.<br><br>You can view it at the following url: <a href="https://www.ippc.int/en/qa/">https://www.ippc.int/en/qa/</a><br><br>International Plant Protection Convention team </p></body></html>'
                notifificationmessage = mail.EmailMessage(subject,textmessage,'ippc@fao.org',  emailto_all, ['paola.sentinelli@fao.org'])
                notifificationmessage.content_subtype = "html"  
                sent =notifificationmessage.send()
                
                return admin.ModelAdmin.save_form(self, request, form, change)
            elif  request.POST['questiondiscard'] == '3':  
                emailto_all = []
                user_obj=User.objects.get(id= request.POST['user'])
                emailto_all.append(str(user_obj.email))
                
                subject='IRSS - Q&A Forum automatic notification: your question has been rejected.'    
            
                textmessage='<html><body><p>Dear IPPC user,<br><br>Your question has been reviewed and has been rejected.<br><br>International Plant Protection Convention team </p></body></html>'

                notifificationmessage = mail.EmailMessage(subject,textmessage,'ippc@fao.org',  emailto_all, ['paola.sentinelli@fao.org'])
                notifificationmessage.content_subtype = "html"  
                sent =notifificationmessage.send()
                return admin.ModelAdmin.save_form(self, request, form, change)
        else:
            return admin.ModelAdmin.save_form(self, request, form, change)
    
admin.site.register(QAQuestion, QAQuestionAdmin)

   
class MyQAAnswerAdminForm(forms.ModelForm):
    class Meta:
        model = QAAnswer
        widgets = {  'description':MarkdownWidget() 
}
class QAAnswerAdmin(admin.ModelAdmin):
    form = MyQAAnswerAdminForm
    fieldsets = [
        ('Answer text', {'fields': ['answertext'], 'classes': ['nocollapse']}),
        ('question', {'fields': ['question'], 'classes': ['nocollapse']}),
        ('publish_date', {'fields': ['publish_date'], 'classes': ['nocollapse']}),
        ('Author', {'fields': ['user'], 'classes': ['nocollapse']}),
        ('Status', {'fields': ['status'], 'classes': ['nocollapse']}),
        ('Best answer', {'fields': ['bestanswer'], 'classes': ['nocollapse']}),
        ('Publish or Reject answer', {'fields': ['answerdiscard'], 'classes': ['collapse']}),
    ]
    list_display = ('question','answertext', 'publish_date','user','status','answerdiscard')
    search_fields = ['description']
    list_filter = ['publish_date','description','status','answerdiscard']
   
    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        admin.ModelAdmin.save_form(self, request, form, change)
        # Answer published
        
        if request.POST['answerdiscard']!=None:
            if request.POST['answerdiscard'] == '2':  
                emailto_all = []
                user_obj=User.objects.get(id= request.POST['user'])
                emailto_all.append(str(user_obj.email))
                subject='IRSS - Q&A Forum automatic notification: your answer has been published.'    
                textmessage='<html><body><p>Dear IPPC user,<br><br>Your answer has been reviewed and now has been published.<br><br>You can view it at the following url: <a href="https://www.ippc.int/en/qa/'+str(request.POST['question'])+'/answers/">https://www.ippc.int/en/qa/'+str(request.POST['question'])+'/answers/</a><br><br>International Plant Protection Convention team </p></body></html>'
                notifificationmessage = mail.EmailMessage(subject,textmessage,'ippc@fao.org',  emailto_all, ['paola.sentinelli@fao.org'])
                notifificationmessage.content_subtype = "html"  
                sent =notifificationmessage.send()
                
                question = get_object_or_404(QAQuestion,  pk=request.POST['question'])
                emailto_all2 = []
                user_obj2=User.objects.get(id= question.user.id)
                emailto_all2.append(str(user_obj2.email))
               
                subject2='IRSS - Q&A Forum automatic notification: an answer to your question has been published.'    
                textmessage2='<html><body><p>Dear IPPC user,<br><br>An answer to your question has been published after being reviewed.<br><br>You can view it at the following url: <a href="https://www.ippc.int/en/qa/'+str(request.POST['question'])+'/answers/">https://www.ippc.int/en/qa/'+str(request.POST['question'])+'/answers/</a><br><br>International Plant Protection Convention team </p></body></html>'
                notifificationmessage2 = mail.EmailMessage(subject2,textmessage2,'ippc@fao.org',  emailto_all2, ['paola.sentinelli@fao.org'])
                notifificationmessage2.content_subtype = "html"  
                sent =notifificationmessage2.send()
                
                return admin.ModelAdmin.save_form(self, request, form, change)
            elif  request.POST['answerdiscard'] == '3':  
                emailto_all = []
                user_obj=User.objects.get(id= request.POST['user'])
                emailto_all.append(str(user_obj.email))
                
                subject='IRSS - Q&A Forum automatic notification: your answer has been rejected.'    
                
                textmessage='<html><body><p>Dear IPPC user,<br><br>Your answer to the <a href="https://www.ippc.int/en/qa/'+str(request.POST['question'])+'/answers/">question</a> has been reviewed and has been rejected.<br><br>International Plant Protection Convention team </p></body></html>'

                notifificationmessage = mail.EmailMessage(subject,textmessage,'ippc@fao.org',  emailto_all, ['paola.sentinelli@fao.org'])
                notifificationmessage.content_subtype = "html"  
                sent =notifificationmessage.send()
                return admin.ModelAdmin.save_form(self, request, form, change)
        else:
            return admin.ModelAdmin.save_form(self, request, form, change)
        
        
      
admin.site.register(QAAnswer, QAAnswerAdmin)


class MyIssueKeywordsRelateAdminForm(forms.ModelForm):
    class Meta:
        model = IssueKeywordsRelate
        widgets = {
          'issuename': autocomplete_light.MultipleChoiceWidget ('IssueKeywordAutocomplete'),
          }


class IssueKeywordsRelateAdmin(admin.ModelAdmin):
    form = MyIssueKeywordsRelateAdminForm
    save_on_top = True
admin.site.register(IssueKeywordsRelate, IssueKeywordsRelateAdmin)

class MyCommodityKeywordsRelateAdminForm(forms.ModelForm):
    class Meta:
        model = CommodityKeywordsRelate
        widgets = {
          'commname': autocomplete_light.MultipleChoiceWidget ('CommodityKeywordAutocomplete'),
          }

class CommodityKeywordsRelateAdmin(admin.ModelAdmin):
    form = MyCommodityKeywordsRelateAdminForm
    save_on_top = True
admin.site.register(CommodityKeywordsRelate, CommodityKeywordsRelateAdmin)   




class PublicationFileInline(admin.TabularInline):
    model = PublicationFile
    formset = inlineformset_factory(Publication,  PublicationFile,extra=1)
    
class PublicationUrlInline(admin.TabularInline):
    model = PublicationUrl
    formset = inlineformset_factory(Publication, PublicationUrl,extra=1)

   
class PublicationAdmin(admin.ModelAdmin):
    inlines = [PublicationFileInline,PublicationUrlInline]
    save_on_top = True
    list_display = ('title',  'modify_date')
    list_filter = ('title',  'modify_date')
    prepopulated_fields = { 'slug': ['title']}
    search_fields = ['title', 'short_description', 'slug', 'file_en', 'file_es', 'file_ar', 'file_ru', 'file_zh', 'file_fr']

    def queryset(self, request):
        qs = super(PublicationAdmin, self).queryset(request)
        return qs.filter(is_version=False)
    
admin.site.register(Publication, PublicationAdmin)

class PublicationInline(StackedDynamicInlineAdmin):
    inlines = [PublicationFileInline,PublicationUrlInline, ]
    model = Publication
    prepopulated_fields = { 'slug': ['title'] }
    

class TransPublicationLibraryPageAdmin(StackedDynamicInlineAdmin):
    model = TransPublicationLibraryPage
    fields = ("lang", "title", "content")

from django.http import HttpResponseRedirect

class PublicationLibraryAdmin(PageAdmin):
    inlines = (PublicationInline, TransPublicationLibraryPageAdmin,)
admin.site.register(PublicationLibrary, PublicationLibraryAdmin)


#class TransReportingObligationAdmin(StackedDynamicInlineAdmin):
#    model = TransReportingObligation
#    fields = ("lang", "title", "short_description")




# Country Pages ----------------- 
# http://mezzanine.jupo.org/docs/content-architecture.html#creating-custom-content-types
countrypages_extra_fieldsets = ((None, {"fields": ("name", "country_slug", "iso", "iso3", "contact_point", "editors", "cp_ncp_t_type", "region", "cn_flag", "accepted_epporeport", "accepted_epporeport_date", )}),)

def response_change(self, request, obj):
    print('ccccccccccccccccccccccccc')
    if not '_continue' in request.POST:
        return HttpResponseRedirect("https://www.ippc.int/en/core-activities/governance/")
    else:
        return super(PublicationLibraryPageAdmin, self).response_change(request, obj)

class OCPHistoryInline(admin.TabularInline):
    model = OCPHistory
    formset = inlineformset_factory(CountryPage,  OCPHistory,extra=1)
class CnEditorsHistoryInLine(admin.TabularInline):
    model = CnEditorsHistory
    formset = inlineformset_factory(CountryPage,  CnEditorsHistory,extra=1)
       
class CountryPageAdmin(PageAdmin):
    fieldsets = deepcopy(PageAdmin.fieldsets) + countrypages_extra_fieldsets
    inlines = (OCPHistoryInline,CnEditorsHistoryInLine)
    prepopulated_fields = { 'country_slug': ['name'] }
    # list_display = ('continent','name','iso','iso3', 'languages', 'currency_name')
    # list_display_links = ('name',)

admin.site.register(CountryPage, CountryPageAdmin)

partnerspages_extra_fieldsets = ((None, {"fields": ("name","content", "short_description", "partner_slug",  "contact_point", "editors", )}),)

 
class PartnersContactPointHistoryInline(admin.TabularInline):
    model = PartnersContactPointHistory
    formset = inlineformset_factory(PartnersPage,  PartnersContactPointHistory,extra=1)
    
class PartnersEditorHistoryInLine(admin.TabularInline):
    model = PartnersEditorHistory
    formset = inlineformset_factory(PartnersPage,  PartnersEditorHistory,extra=1)
  
class PartnersPageAdmin(PageAdmin):
    fieldsets = deepcopy(PageAdmin.fieldsets) + partnerspages_extra_fieldsets
    inlines = (PartnersContactPointHistoryInline,PartnersEditorHistoryInLine)
    prepopulated_fields = { 'partner_slug': ['name'] }
    # list_display = ('continent','name','iso','iso3', 'languages', 'currency_name')
    # list_display_links = ('name',)

admin.site.register(PartnersPage, PartnersPageAdmin)


class PollChoiceInline(admin.TabularInline):
    model = Poll_Choice
    extra = 2
    
class MyPollAdminForm(forms.ModelForm):
    class Meta:
        model = Poll
#        widgets = {
#          'polltext':MarkdownWidget() 
#         # models.TextField: {'widget': },
#        }


class PollAdmin(admin.ModelAdmin):
    form = MyPollAdminForm
    fieldsets = [
        (None,               {'fields': ['question']}),
        (None,               {'fields': ['polltext'], 'classes': ['Textarea']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ('Closing Date', {'fields': ['closing_date'], 'classes': ['collapse']}),
        ('Groups', {'fields': ['userspoll'], 'classes': ['collapse']}),
        ('Users', {'fields': ['groupspoll'], 'classes': ['collapse']}),
       
    ]
    
    list_display = ('question', 'pub_date','closing_date')
    inlines = [PollChoiceInline]
    search_fields = ['question']
    list_filter = ['pub_date','question']
	
admin.site.register(Poll, PollAdmin)


# Work Area Pages -----------------

workareapages_extra_fieldsets = ((None, {"fields": ("users", "groups", "content")}),)
# class WorkAreaFileInline(admin.TabularInline):
#     model = WorkAreaPage
class WorkAreaPageAdmin(PageAdmin):
    # inlines = (WorkAreaFileInline,)
    fieldsets = deepcopy(PageAdmin.fieldsets) + workareapages_extra_fieldsets

admin.site.register(WorkAreaPage, WorkAreaPageAdmin)


# Pest Reports -----------------

class PestStatusAdmin(admin.ModelAdmin):
    """Options for the pest status field of Pest Reports"""
    save_on_top = True
        
class MyPestReportAdminForm(forms.ModelForm):
    class Meta:
        model = PestReport
        widgets = {
          'pest_identity': autocomplete_light.ChoiceWidget ('EppoCodeAutocomplete'),
          }
class PestReportFileInline(admin.TabularInline):
    model = PestReportFile
    formset = inlineformset_factory(PestReport,  PestReportFile,extra=1)
    
class PestReportUrlInline(admin.TabularInline):
    model = PestReportUrl
    formset = inlineformset_factory(PestReport, PestReportUrl,extra=1)
   
class PestReportAdmin(admin.ModelAdmin):
    form = MyPestReportAdminForm
    # http://stackoverflow.com/a/8393130
    # def has_add_permission(self, request):
    #     return request.user.groups.filter(name='Developers').exists()
    # 
    # def has_change_permission(self, request, obj=None):
    #     return request.user.groups.filter(name='Developers').exists()
    # 
    # def has_delete_permission(self, request, obj=None):
    #     return request.user.groups.filter(name='Developers').exists()
    inlines = [PestReportFileInline,PestReportUrlInline ]
    save_on_top = True
    list_display = ('title', 'publish_date', 'modify_date', 'status', 'country')
    list_filter = ('title', 'publish_date', 'modify_date', 'status', 'country')
    search_fields = ('title', 'summary')
    prepopulated_fields = { 'slug': ['title'] }

admin.site.register(PestStatus, PestStatusAdmin)
admin.site.register(PestReport, PestReportAdmin)

class PreferredLanguagesAdmin(admin.ModelAdmin):
    """Options for the PreferredLanguages field of users"""
    save_on_top = True
admin.site.register(PreferredLanguages, PreferredLanguagesAdmin)

class ContactTypeAdmin(admin.ModelAdmin):
    """Options for the pest status field of Pest Reports"""
    save_on_top = True
admin.site.register(ContactType, ContactTypeAdmin)


class DraftProtocolAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title','publish_date')
    list_filter = ('title','publish_date')
    search_fields = ('title','publish_date')
admin.site.register(DraftProtocol,DraftProtocolAdmin)

class EppoCodeAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('codename', 'code', 'codeparent')
    list_filter = ('codename','code')
    search_fields = ('codename', 'code')
admin.site.register(EppoCode, EppoCodeAdmin)


class IssueKeywordAdmin(admin.ModelAdmin):
    save_on_top = True
admin.site.register(IssueKeyword, IssueKeywordAdmin)

class CommodityKeywordAdmin(admin.ModelAdmin):
    save_on_top = True
admin.site.register(CommodityKeyword, CommodityKeywordAdmin)

   
class ReportingObligationFileInline(admin.TabularInline):
    model = ReportingObligation_File
    formset = inlineformset_factory(ReportingObligation,  ReportingObligation_File,extra=1)
    
class ReportingObligationUrlInline(admin.TabularInline):
    model = ReportingObligationUrl
    formset = inlineformset_factory(ReportingObligation, ReportingObligationUrl,extra=1)
 
class ReportingObligationAdmin(admin.ModelAdmin):
    inlines = [ReportingObligationFileInline,ReportingObligationUrlInline,]# TransReportingObligationAdmin
    save_on_top = True
    list_display = ('title', 'publication_date', 'modify_date',   'country')
    list_filter = ('title', 'publication_date', 'modify_date',  'country')
    search_fields = ('title', 'short_description')
    prepopulated_fields = { 'slug': ['title'] }
admin.site.register(ReportingObligation, ReportingObligationAdmin)


class EventReportingFileInline(admin.TabularInline):
    model = EventreportingFile
    formset = inlineformset_factory(EventReporting,  EventreportingFile,extra=1)
    
class EventReportingUrlInline(admin.TabularInline):
    model = EventreportingUrl
    formset = inlineformset_factory(EventReporting,  EventreportingUrl,extra=1)
      
class EventReportingAdmin(admin.ModelAdmin):
    inlines = [EventReportingFileInline,EventReportingUrlInline ]
    save_on_top = True
    list_display = ('title', 'publication_date', 'modify_date',   'country')
    list_filter = ('title', 'publication_date', 'modify_date',  'country')
    search_fields = ('title', 'short_description')
    prepopulated_fields = { 'slug': ['title'] }
admin.site.register(EventReporting, EventReportingAdmin)

class WebsiteUrlInline(admin.TabularInline):
    model = WebsiteUrl
    formset = inlineformset_factory(Website, WebsiteUrl,extra=1)

class WebsiteAdmin(admin.ModelAdmin):
    inlines = [WebsiteUrlInline ]
    save_on_top = True
    list_display = ('title', 'modify_date',   'country')
    list_filter = ('title',   'modify_date',  'country')
    search_fields = ('title', 'short_description')
    prepopulated_fields = { 'slug': ['title'] }
admin.site.register(Website, WebsiteAdmin)

class PartnersWebsiteUrlInline(admin.TabularInline):
    model = PartnersWebsiteUrl
    formset = inlineformset_factory(PartnersWebsite, PartnersWebsiteUrl,extra=1)

class PartnersWebsiteAdmin(admin.ModelAdmin):
    inlines = [PartnersWebsiteUrlInline ]
    save_on_top = True
    list_display = ('title', 'modify_date',   'partners')
    list_filter = ('title',   'modify_date',  'partners')
    search_fields = ('title', 'short_description')
    prepopulated_fields = { 'slug': ['title'] }
admin.site.register(PartnersWebsite, PartnersWebsiteAdmin)

class PestFreeAreaFileInline(admin.TabularInline):
    model = PestFreeAreaFile
    formset = inlineformset_factory(PestFreeArea,  PestFreeAreaFile,extra=1)
    
class PestFreeAreaUrlInline(admin.TabularInline):
    model = PestFreeAreaUrl
    formset = inlineformset_factory(PestFreeArea, PestFreeAreaUrl,extra=1)
    
class PestFreeAreaAdmin(admin.ModelAdmin):
    inlines = [PestFreeAreaFileInline,PestFreeAreaUrlInline, ]
    save_on_top = True
    list_display = ('title', 'publication_date', 'modify_date',   'country')
    list_filter = ('title', 'publication_date', 'modify_date',  'country')
    search_fields = ('title', 'short_description')
    prepopulated_fields = { 'slug': ['title'] }
admin.site.register(PestFreeArea, PestFreeAreaAdmin)

class CnPublicationFileInline(admin.TabularInline):
    model = CnPublicationFile
    formset = inlineformset_factory(CnPublication,  CnPublicationFile,extra=1)
    
class CnPublicationUrlInline(admin.TabularInline):
    model = CnPublicationUrl
    formset = inlineformset_factory(CnPublication, CnPublicationUrl,extra=1)

class CnPublicationAdmin(admin.ModelAdmin):
    inlines = [CnPublicationFileInline,CnPublicationUrlInline]
    save_on_top = True
    list_display = ('title', 'publication_date', 'modify_date',   'country')
    list_filter = ('title', 'publication_date', 'modify_date',  'country')
    search_fields = ('title', 'short_description')
    prepopulated_fields = { 'slug': ['title'] }
admin.site.register(CnPublication, CnPublicationAdmin)   


class PartnersPublicationFileInline(admin.TabularInline):
    model = PartnersPublicationFile
    formset = inlineformset_factory(PartnersPublication,  PartnersPublicationFile,extra=1)
    
class PartnersPublicationUrlInline(admin.TabularInline):
    model = PartnersPublicationUrl
    formset = inlineformset_factory(PartnersPublication, PartnersPublicationUrl,extra=1)

class PartnersPublicationAdmin(admin.ModelAdmin):
    inlines = [PartnersPublicationFileInline,PartnersPublicationUrlInline]
    save_on_top = True
    list_display = ('title', 'publication_date', 'modify_date',   'partners')
    list_filter = ('title', 'publication_date', 'modify_date',  'partners')
    search_fields = ('title', 'short_description')
    prepopulated_fields = { 'slug': ['title'] }
admin.site.register(PartnersPublication, PartnersPublicationAdmin)  





class ImplementationISPMFileInline(admin.TabularInline):
    model = ImplementationISPMFile
    formset = inlineformset_factory(ImplementationISPM,  ImplementationISPMFile,extra=1)
    
class ImplementationISPMUrlInline(admin.TabularInline):
    model = ImplementationISPMUrl
    formset = inlineformset_factory(ImplementationISPM, ImplementationISPMUrl,extra=1)    

class ImplementationISPMAdmin(admin.ModelAdmin):
    inlines = [ImplementationISPMFileInline,ImplementationISPMUrlInline ]
    save_on_top = True
    list_display = ('title', 'publication_date', 'modify_date',   'country')
    list_filter = ('title', 'publication_date', 'modify_date',  'country')
    search_fields = ('title', 'short_description')
    prepopulated_fields = { 'slug': ['title'] }
admin.site.register(ImplementationISPM, ImplementationISPMAdmin)

class ImplementationISPMVersionAdmin(admin.ModelAdmin):
    """Options for ImplementationISPMVersion field of ImplementationISPM"""
    save_on_top = True
admin.site.register(ImplementationISPMVersion, ImplementationISPMVersionAdmin)  

class CountryNewsFileInline(admin.TabularInline):
    model =  CountryNewsFile
    formset = inlineformset_factory( CountryNews,   CountryNewsFile,extra=1)
    
class  CountryNewsUrlInline(admin.TabularInline):
    model =  CountryNewsUrl
    formset = inlineformset_factory( CountryNews,  CountryNewsUrl,extra=1)
 
class  CountryNewsAdmin(admin.ModelAdmin):
    inlines = [CountryNewsFileInline,CountryNewsUrlInline, ]
    save_on_top = True
    list_display = ('title', 'publication_date', 'modify_date',   'country')
    list_filter = ('title', 'publication_date', 'modify_date',  'country')
    search_fields = ('title', 'short_description')
    prepopulated_fields = { 'slug': ['title'] }
admin.site.register( CountryNews,  CountryNewsAdmin)

class PartnersNewsFileInline(admin.TabularInline):
    model =  PartnersNewsFile
    formset = inlineformset_factory( PartnersNews,   PartnersNewsFile,extra=1)
    
class  PartnersNewsUrlInline(admin.TabularInline):
    model =  PartnersNewsUrl
    formset = inlineformset_factory( PartnersNews,  PartnersNewsUrl,extra=1)
 
class  PartnersNewsAdmin(admin.ModelAdmin):
    inlines = [PartnersNewsFileInline,PartnersNewsUrlInline, ]
    save_on_top = True
    list_display = ('title', 'publication_date', 'modify_date',   'partners')
    list_filter = ('title', 'publication_date', 'modify_date',  'partners')
    search_fields = ('title', 'short_description')
   
admin.site.register( PartnersNews,  PartnersNewsAdmin)

#NEW
class MyFAQsCategoryAdminForm(forms.ModelForm):
    class Meta:
        model = FAQsCategory

class TransFAQsCategoryAdmin(StackedDynamicInlineAdmin):
    model = TransFAQsCategory
    fields = ("lang", "title", )
    
class FAQsCategoryAdmin(admin.ModelAdmin):
    form = MyFAQsCategoryAdminForm
    save_on_top = True
    list_display = ('id','title','faqcat_oder')
    #list_filter = ('faqcategory_title')
   # search_fields = ('faqcategory_title')
    prepopulated_fields = { 'slug': ['title'] } 
    inlines = ( TransFAQsCategoryAdmin,)
admin.site.register(FAQsCategory, FAQsCategoryAdmin)




class MyFAQsItemAdminForm(forms.ModelForm):
    class Meta:
        model = FAQsItem
        
class TransFAQsItemAdmin(StackedDynamicInlineAdmin):
    model = TransFAQsItem
    fields = ("lang","title", "faq_description","faq_anchor" )
    
class FAQsItemAdmin(admin.ModelAdmin):
    form = MyFAQsItemAdminForm
    save_on_top = True
    list_display = ('title', 'faqcategory', 'faq_description',   'publish_date')
    list_filter = ('title', 'faqcategory', 'faq_description',  'publish_date')
    inlines = ( TransFAQsItemAdmin,)
    search_fields = ('title', 'faqcategory')
    prepopulated_fields = { 'slug': ['title'] }
	
admin.site.register(FAQsItem, FAQsItemAdmin)

class IRSSActivityFileInline(admin.TabularInline):
    model = IRSSActivityFile
    formset = inlineformset_factory(IRSSActivity,  IRSSActivityFile,extra=1)

class IRSSActivityAdmin(admin.ModelAdmin):
    inlines = [IRSSActivityFileInline,]
    save_on_top = True
    list_display = ('title', 'publish_date', 'modify_date',  )
    list_filter = ('title', 'publish_date', 'modify_date', )
    search_fields = ('title', 'description')
    
admin.site.register(IRSSActivity, IRSSActivityAdmin)   

class UserMembershipHistoryAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('user', 'group', 'start_date','end_date' ,'countrypage','partnerpage','file' )
    list_filter = ('user', 'group',  )
    search_fields = ('user', 'group')
    
admin.site.register(UserMembershipHistory, UserMembershipHistoryAdmin)   


# Translatable user-content  -----------------
if "mezzanine.pages" in settings.INSTALLED_APPS:


    #
    # Richtext
    #
    class TransInline(TabularDynamicInlineAdmin):
        model  = TransRichTextPage
        fields = ("lang", "title", "content")

    class TransPageAdmin(PageAdmin):
        inlines   = (TransInline,)

    admin.site.unregister(RichTextPage)
    admin.site.register(RichTextPage, TransPageAdmin)
    


    #
    # Link
    #
    class TransLinkInline(TabularDynamicInlineAdmin):
        model = TransLinkPage
        fields = ("lang", "title", "slug")

    class TransLinkAdmin(LinkAdmin):
        inlines  = (TransLinkInline,)

    admin.site.unregister(Link)
    admin.site.register(Link, TransLinkAdmin)

if "mezzanine.forms" in settings.INSTALLED_APPS:
    from mezzanine.forms.models import Form, Field
    from mezzanine.forms.admin import FormAdmin, FieldAdmin
    from models import TransField, TransForm

    #
    # Form
    #
    class TransFormInline(TabularDynamicInlineAdmin):
        model = TransForm
        fields = ("lang", "title", "content", "button_text", "response")

    class TransFormAdmin(FormAdmin):
        inlines = (FieldAdmin, TransFormInline)

    admin.site.unregister(Form)
    admin.site.register(Form, TransFormAdmin)

    class TransFieldInline(TabularDynamicInlineAdmin):
        model = TransField
        fields = ("lang", "original", "label", "choices", "default", "help_text")

    class TransFieldAdmin(admin.ModelAdmin):
        inlines = (TransFieldInline, )
        fields = ("label", "choices", "default", "help_text")
    admin.site.register(Field, TransFieldAdmin)

    #
    # Gallery
    #
if "mezzanine.galleries" in settings.INSTALLED_APPS:
    from mezzanine.galleries.models import Gallery, GalleryImage
    from mezzanine.galleries.admin import GalleryAdmin, GalleryImageInline
    from models import TransGallery, TransGalleryImage

    class TransGalleryInline(TabularDynamicInlineAdmin):
        model  = TransGallery
        fields = ("lang", "title", "content", )

    class TransGalleryAdmin(GalleryAdmin):
        inlines = (GalleryImageInline, TransGalleryInline, )

    admin.site.unregister(Gallery)
    admin.site.register(Gallery, TransGalleryAdmin)