
from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from news.models import NewsPost, NewsCategory
from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin


newspost_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
newspost_fieldsets[0][1]["fields"].insert(1, "categories")
newspost_fieldsets[0][1]["fields"].extend(["content"])
newspost_list_display = ["title", "user", "status", "admin_link"]
if settings.NEWS_USE_FEATURED_IMAGE:
    newspost_fieldsets[0][1]["fields"].insert(-2, "featured_image")
    newspost_list_display.insert(0, "admin_thumb")
newspost_fieldsets = list(newspost_fieldsets)
newspost_fieldsets.insert(1, (_("Other posts"), {
    "classes": ("collapse-closed",),
    "fields": ("related_posts",)}))
newspost_list_filter = deepcopy(DisplayableAdmin.list_filter) + ("categories",)


class NewsPostAdmin(DisplayableAdmin, OwnableAdmin):
    """
    Admin class for news posts.
    """

    fieldsets = newspost_fieldsets
    list_display = newspost_list_display
    list_filter = newspost_list_filter
    filter_horizontal = ("categories", "related_posts",)

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
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
