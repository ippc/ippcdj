
from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import IyphPost, IyphCategory,TransIyphPost,Chronology,TransChronology,IYPHSteeringCommitteeResource,IYPHToolBoxItem,IYPHToolBoxCategory
from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin,StackedDynamicInlineAdmin

class TransIyphPostAdmin(StackedDynamicInlineAdmin):
    model = TransIyphPost
    fields = ("lang", "title", "content")
    


class TransChronologyAdmin(StackedDynamicInlineAdmin):
    model = TransChronology
    fields = ("lang", "title", "summary")
    
iyphpost_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
iyphpost_fieldsets[0][1]["fields"].insert(1, "categories")
iyphpost_fieldsets[0][1]["fields"].extend(["content"])
iyphpost_list_display = ["title", "user", "status", "admin_link"]
if settings.IYPH_USE_FEATURED_IMAGE:
    iyphpost_fieldsets[0][1]["fields"].insert(-2, "featured_image")
    iyphpost_list_display.insert(0, "admin_thumb")
iyphpost_fieldsets = list(iyphpost_fieldsets)
iyphpost_fieldsets.insert(1, (_("Other posts"), {
    "classes": ("collapse-closed",),
    "fields": ("related_posts",)}))
iyphpost_list_filter = deepcopy(DisplayableAdmin.list_filter) + ("categories",)

#class IyphPostAdmin(DisplayableAdmin, OwnableAdmin):
class IyphPostAdmin(DisplayableAdmin):
    """
    Admin class for iyph posts.
    """

    fieldsets = iyphpost_fieldsets
    list_display = iyphpost_list_display
    list_filter = iyphpost_list_filter
    filter_horizontal = ("categories", "related_posts",)
    inlines = [ TransIyphPostAdmin]
   
    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        #OwnableAdmin.save_form(self, request, form, change)
        if change==False:
            obj = form.save(commit=False)
            if obj.user_id is None:
                obj.user = request.user 
            DisplayableAdmin.save_form(self, request, form, change)
        else: 
            DisplayableAdmin.save_form(self, request, form, change)

        return DisplayableAdmin.save_form(self, request, form, change)


  


class IyphCategoryAdmin(admin.ModelAdmin):
    """
    Admin class for iyph categories. Hides itself from the admin menu
    unless explicitly specified.
    """

    fieldsets = ((None, {"fields": ("title",)}),)

    def in_menu(self):
        """
        Hide from the admin menu unless explicitly set in ``ADMIN_MENU_ORDER``.
        """
        for (name, items) in settings.ADMIN_MENU_ORDER:
            if "iyph.IyphCategory" in items:
                return True
        return False


admin.site.register(IyphPost, IyphPostAdmin)
admin.site.register(IyphCategory, IyphCategoryAdmin)

class ChronologyAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title', 'publish_date', 'modify_date', 'status')
    list_filter = ('title', 'publish_date', 'modify_date', 'status')
    search_fields = ('title', 'summary')
    prepopulated_fields = { 'slug': ['title'] }
    inlines = [ TransChronologyAdmin]
   
admin.site.register(Chronology, ChronologyAdmin)

class IYPHSteeringCommitteeResourceAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title', 'publish_date', 'modify_date', 'status')
    list_filter = ('title', 'publish_date', 'modify_date', 'status')
    search_fields = ('title', 'summary')
    prepopulated_fields = { 'slug': ['title'] }
     
admin.site.register(IYPHSteeringCommitteeResource, IYPHSteeringCommitteeResourceAdmin)

class IYPHToolBoxItemAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title', 'publish_date', 'modify_date', 'status')
    list_filter = ('title', 'publish_date', 'modify_date', 'status')
    search_fields = ('title', 'summary')
    prepopulated_fields = { 'slug': ['title'] }
     
admin.site.register(IYPHToolBoxItem, IYPHToolBoxItemAdmin)

class IYPHToolBoxCategoryAdmin(admin.ModelAdmin):
    """
    Admin class for iyph categories. Hides itself from the admin menu
    unless explicitly specified.
    """

    fieldsets = ((None, {"fields": ("title",)}),)

    def in_menu(self):
        """
        Hide from the admin menu unless explicitly set in ``ADMIN_MENU_ORDER``.
        """
        for (name, items) in settings.ADMIN_MENU_ORDER:
            if "iyph.IYPHToolBoxCategory" in items:
                return True
        return False



admin.site.register(IYPHToolBoxCategory, IYPHToolBoxCategoryAdmin)