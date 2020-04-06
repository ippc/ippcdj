
from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from news.models import NewsPost, NewsCategory,TransNewsPost
from ippc.models import MassEmailUtilityMessage
from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin,StackedDynamicInlineAdmin
from django.contrib.auth.models import User,Group
from django.shortcuts import get_object_or_404
from django.core import mail
from django.core.mail import send_mail

from django.template.defaultfilters import slugify

from datetime import datetime
from django_markdown.widgets import MarkdownWidget
from django import forms
from django_markdown.admin import MarkdownModelAdmin
from django_markdown.widgets import AdminMarkdownWidget

class TransNewsPostAdmin(StackedDynamicInlineAdmin):
    model = TransNewsPost
    fields = ("lang", "title","caption_image", "content","related_info")

newspost_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
newspost_fieldsets[0][1]["fields"].insert(1, "categories")
newspost_fieldsets[0][1]["fields"].extend(["caption_image"])
newspost_fieldsets[0][1]["fields"].extend(["content"])
newspost_fieldsets[0][1]["fields"].extend(["related_info"])

newspost_list_display = ["title", "user","publish_date", "status", "admin_link"]
if settings.NEWS_USE_FEATURED_IMAGE:
    newspost_fieldsets[0][1]["fields"].insert(-2, "featured_image")
    newspost_list_display.insert(0, "admin_thumb")
newspost_fieldsets = list(newspost_fieldsets)
newspost_fieldsets.insert(1, (_("Other posts"), {
    "classes": ("collapse-closed",),
    "fields": ("related_posts",)}))
newspost_list_filter = deepcopy(DisplayableAdmin.list_filter) + ("categories",)

class NewsPostAdminForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        widgets = { 'related_info':AdminMarkdownWidget() 

}
#class NewsPostAdmin(DisplayableAdmin, OwnableAdmin):
class NewsPostAdmin(DisplayableAdmin):
    """
    Admin class for news posts.
    """
    form = NewsPostAdminForm
    fieldsets = newspost_fieldsets
    list_display = newspost_list_display
    list_filter = newspost_list_filter
    filter_horizontal = ("categories", "related_posts",)
    inlines = [ TransNewsPostAdmin]
    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        #OwnableAdmin.save_form(self, request, form, change)
        send=False
        
        news_slug=''
        if change==True:
          if request.POST['slug'] != None:
            news_slug=request.POST['slug']
            n_obj=get_object_or_404(NewsPost,slug=request.POST['slug']) 
            if n_obj.status == 1 and request.POST['status']=='2':
               send=True
            
        if change==False:
            slug1=slugify(request.POST['title'])
            alreadynews = NewsPost.objects.filter(slug__icontains=slug1)
            if alreadynews.count()>0:
                old2slug=alreadynews[0].slug
                intslug=old2slug.replace(slug1+"-","")
                intslug1=int(intslug)+1
                news_slug=slug1+"-"+str(intslug1)
            else:
                news_slug= slug1
           
            obj = form.save(commit=False)
           
            if obj.user_id is None:
                obj.user = request.user 
                obj.slug = news_slug 
            DisplayableAdmin.save_form(self, request, form, change)
        else: 
            DisplayableAdmin.save_form(self, request, form, change)
        
            
        if change==False and request.POST['status'] == '2'  :
            send=True
            
        #new news post send notifications to Secretariat
        if send==True  :
            emailto_all = []
            emailto_all_news = []
            emailto_all_announc = []
            
            group=Group.objects.get(name="News Notification group")
            users = group.user_set.all()
            for u in users:
               user_obj=User.objects.get(username=u)
               user_email=user_obj.email
               emailto_all_news.append(str(user_email))
            group2=Group.objects.get(name="Announcement Notification group")
            users2 = group2.user_set.all()
            for u in users2:
               user_obj=User.objects.get(username=u)
               user_email=user_obj.email
               emailto_all_announc.append(str(user_email))
            category=None
            try:
                category=get_object_or_404(NewsCategory, id=request.POST['categories']).title 
            except:
                print("###################error in category ")
            
            if(category!=None and (category == 'Announcements' or category == 'IPPC news' )):
                pdate= request.POST['publish_date_0']
                d = datetime.strptime(pdate, '%Y-%m-%d')
                day_string = d.strftime('%d-%m-%Y')
                subject=''
                text=''
                if  category == 'IPPC news':
                    subject='IPPC News has been posted'   
                    emailto_all=emailto_all_news
                    text='<html><body><p>Dear IPPC User,</p><p>a new IPPC News has been posted on the International Phytosanitary Portal (IPP):<br><br> <b>'+ request.POST['title']+'</b></p><p>You can view it from '+day_string+' at the following url: <a href="http://www.ippc.int/news/'+news_slug+'">https://www.ippc.int/news/'+news_slug+'</a></p><p><br>Kind regards,<br><br>The International Plant Protection Convention Secretariat</p><p><br><br>If you want to <b>un-subscribe</b> from the News notifications <b>login to IPP</b>, then go <a href="http://www.ippc.int/news/category/ippcnews/"><b>here</b></a> and click on the button <b>un-subscribe</b>.</p></body></html>'
                elif  category == 'Announcements':
                    subject='IPPC announcement has been posted'
                    emailto_all=emailto_all_announc
                    text='<html><body><p>Dear IPPC User,</p><p>a new IPPC announcement has been posted on the International Phytosanitary Portal (IPP):<br><br> <b>'+ request.POST['title']+'</b></p><p>You can view it from '+day_string+' at the following url: <a href="http://www.ippc.int/news/'+news_slug+'">https://www.ippc.int/news/'+news_slug+'</a></p><p><br>Kind regards,<br><br>The International Plant Protection Convention Secretariat</p><p><br><br>If you want to <b>un-subscribe</b> from the Announcements notifications <b>login to IPP</b>, then go <a href="http://www.ippc.int/news/category/announcements/"><b>here</b></a> and click on the button <b>un-subscribe</b>.</p></body></html>'
                
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
    
                #######################################
                #notifificationmessage = mail.EmailMessage(subject,text,'ippc@fao.org',  emailto_all, ['paola.sentinelli@fao.org'])
                #notifificationmessage.content_subtype = "html"  
                #sent =notifificationmessage.send()
        
        return DisplayableAdmin.save_form(self, request, form, change)

class NewsCategoryAdmin(admin.ModelAdmin):
    """
    Admin class for news categories. Hides itself from the admin menu
    unless explicitly specified.
    """

    fieldsets = ((None, {"fields": ("title",)}),)

    def in_menu(self):
        """
        Hide from the admin menu unless explicitly set in ``ADMIN_MENU_ORDER``.
        """
        for (name, items) in settings.ADMIN_MENU_ORDER:
            if "news.NewsCategory" in items:
                return True
        return False


admin.site.register(NewsPost, NewsPostAdmin)
admin.site.register(NewsCategory, NewsCategoryAdmin)
