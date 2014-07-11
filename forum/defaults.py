"""
Default settings for the ``ippc.forum`` app. Each of these can be
overridden in your project's settings module, just like regular
Django settings. The ``editable`` argument for each controls whether
the setting is editable via Django's admin.

Thought should be given to how a setting is actually used before
making it editable, as it may be inappropriate - for example settings
that are only read during startup shouldn't be editable, since changing
them would require an application reload.
"""

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import register_setting


register_setting(
    name="forum_USE_FEATURED_IMAGE",
    description=_("Enable featured images in forum posts"),
    editable=False,
    default=False,
)

_FORUM_URLS_DATE_FORMAT = ""
if getattr(settings, "FORUM_URLS_USE_DATE", False):
    _FORUM_URLS_DATE_FORMAT = "day"
    from warnings import warn
    warn("FORUM_URLS_USE_DATE setting is deprecated, please use the "
        "FORUM_URLS_DATE_FORMAT setting with a value of 'year', 'month', "
        "or 'day'.")

register_setting(
    name="FORUM_URLS_DATE_FORMAT",
    label=_("Forum post URL date format"),
    description=_("A string containing the value ``year``, ``month``, or "
        "``day``, which controls the granularity of the date portion in the "
        "URL for each forum post. Eg: ``year`` will define URLs in the format "
        "/forum/yyyy/slug/, while ``day`` will define URLs with the format "
        "/forum/yyyy/mm/dd/slug/. An empty string means the URLs will only "
        "use the slug, and not contain any portion of the date at all."),
    editable=False,
    default=_FORUM_URLS_DATE_FORMAT,
)

register_setting(
    name="FORUM_POST_PER_PAGE",
    label=_("Forum posts per page"),
    description=_("Number of forum posts shown on a forum listing page."),
    editable=True,
    default=5,
)

register_setting(
    name="forum_RSS_LIMIT",
    label=_("Forum posts RSS limit"),
    description=_("Number of most recent forum posts shown in the RSS feed. "
        "Set to ``None`` to display all forum posts in the RSS feed."),
    editable=False,
    default=20,
)

register_setting(
    name="FORUM_SLUG",
    description=_("Slug of the page object for the forum."),
    editable=False,
    default="forum",
)
