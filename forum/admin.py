
from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from .models import ForumPost, ForumCategory,ForumPost_Files
from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin
from django.core import mail
from django.core.mail import send_mail
from django.contrib.auth.models import User,Group
from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory
import markdown
from django.template.defaultfilters import slugify
from ippc.models import  MassEmailUtilityMessage
from django.utils import timezone

forumpost_fieldsets = deepcopy(DisplayableAdmin.fieldsets)

forumpost_fieldsets[0][1]["fields"].insert(1, "categories")
forumpost_fieldsets[0][1]["fields"].extend(["content", "allow_comments", "login_required"])
forumpost_fieldsets[0][1]["fields"].insert(5, "groups")
forumpost_fieldsets[0][1]["fields"].insert(6, "users")
forumpost_fieldsets[0][1]["fields"].insert(7, "notification_groups")
forumpost_list_display = ["title", "user", "status", "admin_link"]
if settings.FORUM_USE_FEATURED_IMAGE:
    forumpost_fieldsets[0][1]["fields"].insert(-2, "featured_image")
    forumpost_list_display.insert(0, "admin_thumb")
forumpost_fieldsets = list(forumpost_fieldsets)
forumpost_fieldsets.insert(1, (_("Other posts"), {
    "classes": ("collapse-closed",),
    "fields": ("related_posts",)}))
forumpost_list_filter = deepcopy(DisplayableAdmin.list_filter) + ("categories",)

class ForumPostFileInline(admin.TabularInline):
    model = ForumPost_Files
    formset = inlineformset_factory(ForumPost, ForumPost_Files,extra=1)
    

#class ForumPostAdmin(DisplayableAdmin,OwnableAdmin):
class ForumPostAdmin(DisplayableAdmin):
    """
    Admin class for forum posts.
    """
    
    fieldsets = forumpost_fieldsets
    list_display = forumpost_list_display
    list_filter = forumpost_list_filter
    filter_horizontal = ("categories", "related_posts",)
    inlines = [ForumPostFileInline]
    
    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        #OwnableAdmin.save_form(self, request, form, change)
        #changed to made all secretariat editor of forum posts
        if change==False:
            obj = form.save(commit=False)
            if obj.user_id is None:
                obj.user = request.user 
            DisplayableAdmin.save_form(self, request, form, change)
        else: 
            DisplayableAdmin.save_form(self, request, form, change)
      
        #new forum post send notifications
        if change==False:
            emailto_all = []
            for g in request.POST.getlist('notification_groups'):
                group=Group.objects.get(id=g)
                users = group.user_set.all()
                for u in users:
                   user_obj=User.objects.get(username=u)
                   user_email=user_obj.email
                   print(user_email)   
                   emailto_all.append(str(user_email))
            
            category=get_object_or_404(ForumCategory, id=request.POST['categories']).title 
            #if(category == 'TPDP Forum'):
                #print('no notifification')
            #else:    
            subject='IPPC FORUM: '+category+' - new discussion: '+request.POST['title']       
            #markdowner = Markdown()
            bodycontent = markdown.markdown(request.POST['content'])


            text='<html><body><p>Dear IPPC user,</p><p>a new discussion has been posted in the '+category+' Forum.</p><p><b>Discussion:</b>'+ request.POST['title']+'</p><p><b>Post:</b></p><p>'+bodycontent+'</p><p>You can view it at the following url: https://www.ippc.int/forum/'+slugify(request.POST['title'])+'</p><p>-- International Plant Protection Convention team </p></body></html>'

            notifificationmessage = mail.EmailMessage(subject,text,'ippc@fao.org',  emailto_all, ['paola.sentinelli@fao.org'])
            notifificationmessage.content_subtype = "html"  
            sent =notifificationmessage.send()
           
        
        return DisplayableAdmin.save_form(self, request, form, change)


class ForumCategoryAdmin(admin.ModelAdmin):
    """
    Admin class for forum categories. Hides itself from the admin menu
    unless explicitly specified.
    """

    fieldsets = ((None, {"fields": ("title",)}),)

    def in_menu(self):
        """
        Hide from the admin menu unless explicitly set in ``ADMIN_MENU_ORDER``.
        """
        for (name, items) in settings.ADMIN_MENU_ORDER:
            if "forum.ForumCategory" in items:
                return True
        return False


admin.site.register(ForumPost, ForumPostAdmin)
admin.site.register(ForumCategory, ForumCategoryAdmin)
