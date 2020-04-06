
from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from mezzanine.conf import settings
from ippc.models import MassEmailUtilityMessage

from django.contrib.auth.models import User,Group
from django.shortcuts import get_object_or_404
from django.core import mail
from django.core.mail import send_mail
from .models import CallsPost, CallsCategory,TransCallsPost
from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin,StackedDynamicInlineAdmin
from datetime import datetime
from django_markdown.widgets import MarkdownWidget
from django import forms
from django_markdown.admin import MarkdownModelAdmin
from django_markdown.widgets import AdminMarkdownWidget


class TransCallsPostAdmin(StackedDynamicInlineAdmin):
    model = TransCallsPost
    fields = ("lang", "title", "content")
    
callspost_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
callspost_fieldsets[0][1]["fields"].insert(1, "categories")
callspost_fieldsets[0][1]["fields"].insert(2, "deadline_date")
callspost_fieldsets[0][1]["fields"].extend(["content"])
callspost_list_display = ["title", "user", "status", "admin_link"]
if settings.CALLS_USE_FEATURED_IMAGE:
    callspost_fieldsets[0][1]["fields"].insert(-2, "featured_image")
    callspost_list_display.insert(0, "admin_thumb")
callspost_fieldsets = list(callspost_fieldsets)
callspost_fieldsets.insert(1, (_("Other posts"), {
    "classes": ("collapse-closed",),
    "fields": ("related_posts",)}))
callspost_list_filter = deepcopy(DisplayableAdmin.list_filter) + ("categories",)





#class CallsPostAdmin(DisplayableAdmin, OwnableAdmin):
class CallsPostAdmin(DisplayableAdmin):
    """
    Admin class for calls posts. 
    """

    fieldsets = callspost_fieldsets
    list_display = callspost_list_display
    list_filter = callspost_list_filter
    inlines = [ TransCallsPostAdmin]
   
    filter_horizontal = ("categories", "related_posts",)

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        #OwnableAdmin.save_form(self, request, form, change)
        send=False
        
        call_slug=''
        if change==True:
          if request.POST['slug'] != None:
            call_slug=request.POST['slug']
            n_obj=get_object_or_404(CallsPost,slug=request.POST['slug']) 
            if n_obj.status == 1 and request.POST['status']=='2':
               send=True
            
        if change==False:
            slug1=slugify(request.POST['title'])
            alreadycall = CallsPost.objects.filter(slug__icontains=slug1)
            if alreadycall.count()>0:
                old2slug=alreadycall[0].slug
                intslug=old2slug.replace(slug1+"-","")
                intslug1=int(intslug)+1
                call_slug=slug1+"-"+str(intslug1)
            else:
                call_slug= slug1
            
            obj = form.save(commit=False)
            if obj.user_id is None:
                obj.user = request.user 
            DisplayableAdmin.save_form(self, request, form, change)
        else: 
            DisplayableAdmin.save_form(self, request, form, change)
      
        if change==False and request.POST['status'] == '2'  :
            send=True
            
        #new news post send notifications to Secretariat
        if send==True  :
            emailto_all = []
            
            group=Group.objects.get(name="Calls Notification group")
            users = group.user_set.all()
            for u in users:
               user_obj=User.objects.get(username=u)
               user_email=user_obj.email
               emailto_all.append(str(user_email))
            
            pdate= request.POST['publish_date_0']
            d = datetime.strptime(pdate, '%Y-%m-%d')
            day_string = d.strftime('%d-%m-%Y')
            subject=''
            text=''
         
            subject='IPPC Call has been posted'   
            text='<html><body><p>Dear IPPC User,</p><p>a new IPPC Call has been posted on the International Phytosanitary Portal (IPP):<br><br> <b>'+ request.POST['title']+'</b></p><p>You can view it from '+day_string+' at the following url: <a href="http://www.ippc.int/calls/'+call_slug+'">https://www.ippc.int/calls/'+call_slug+'</a></p><p><br>Kind regards,<br><br>The International Plant Protection Convention Secretariat</p><p><br><br>If you want to <b>un-subscribe</b> from the Calls notifications <b>login to IPP</b>, then go <a href="http://www.ippc.int/calls/"><b>here</b></a> and click on the button <b>un-subscribe</b>.</p></body></html>'
            emailto_all_final=''
            for eee in emailto_all:
                emailto_all_final=emailto_all_final+eee+','

            author = get_object_or_404(User, pk=1652)    
            ############################################
            massemail = MassEmailUtilityMessage()
            massemail.emailfrom = 'ippc@fao.org'
            massemail.emailto = emailto_all_final
            massemail.emailtoISO3 = ''
            massemail.emailcc = ''
            massemail.subject = subject
            massemail.messagebody = text
            massemail.date = datetime.now()
            massemail.sent = 0
            massemail.status = 1
            massemail.not_sentto = emailto_all_final
            massemail.sentto =  ''
            massemail.not_senttoISO3 = ''
            massemail.senttoISO3 = ''
            massemail.author= author
            massemail.massmerge = 0

            massemail.save()

            subnew='MASS EMAIL STORED:'+subject

            notifificationmessage = mail.EmailMessage(subnew,text,'ippc@fao.org',  ['paola.sentinelli@fao.org'], ['paola.sentinelli@fao.org'])
            notifificationmessage.content_subtype = "html"  
            sent =notifificationmessage.send()
                
            #notifificationmessage = mail.EmailMessage(subject,text,'ippc@fao.org',  emailto_all, ['paola.sentinelli@fao.org'])
            #notifificationmessage.content_subtype = "html"  
            #sent =notifificationmessage.send()
      
        return DisplayableAdmin.save_form(self, request, form, change)


  


class CallsCategoryAdmin(admin.ModelAdmin):
    """
    Admin class for calls categories. Hides itself from the admin menu
    unless explicitly specified.
    """

    fieldsets = ((None, {"fields": ("title",)}),)

    def in_menu(self):
        """
        Hide from the admin menu unless explicitly set in ``ADMIN_MENU_ORDER``.
        """
        for (name, items) in settings.ADMIN_MENU_ORDER:
            if "calls.CallsCategory" in items:
                return True
        return False


admin.site.register(CallsPost, CallsPostAdmin)
admin.site.register(CallsCategory, CallsCategoryAdmin)
