
from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import CallsPost, CallsCategory
from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin


callspost_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
callspost_fieldsets[0][1]["fields"].insert(1, "categories")
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


class CallsPostAdmin(DisplayableAdmin, OwnableAdmin):
    """
    Admin class for calls posts.
    """

    fieldsets = callspost_fieldsets
    list_display = callspost_list_display
    list_filter = callspost_list_filter
    filter_horizontal = ("categories", "related_posts",)

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
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
