
from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import ForumPost, ForumCategory
from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin


forumpost_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
forumpost_fieldsets[0][1]["fields"].insert(1, "categories")
forumpost_fieldsets[0][1]["fields"].extend(["content", "allow_comments"])
forumpost_list_display = ["title", "user", "status", "admin_link"]
if settings.FORUM_USE_FEATURED_IMAGE:
    forumpost_fieldsets[0][1]["fields"].insert(-2, "featured_image")
    forumpost_list_display.insert(0, "admin_thumb")
forumpost_fieldsets = list(forumpost_fieldsets)
forumpost_fieldsets.insert(1, (_("Other posts"), {
    "classes": ("collapse-closed",),
    "fields": ("related_posts",)}))
forumpost_list_filter = deepcopy(DisplayableAdmin.list_filter) + ("categories",)


class ForumPostAdmin(DisplayableAdmin, OwnableAdmin):
    """
    Admin class for forum posts.
    """

    fieldsets = forumpost_fieldsets
    list_display = forumpost_list_display
    list_filter = forumpost_list_filter
    filter_horizontal = ("categories", "related_posts",)

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
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
