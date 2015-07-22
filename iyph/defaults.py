"""
Default settings for the ``mezzanine.blog`` app. Each of these can be
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
    name="IYPH_USE_FEATURED_IMAGE",
    description=_("Enable featured images in iyph posts"),
    editable=False,
    default=False,
)

_IYPH_URLS_DATE_FORMAT = ""
if getattr(settings, "IYPH_URLS_USE_DATE", False):
    _IYPH_URLS_DATE_FORMAT = "day"
    from warnings import warn
    warn("IYPH_URLS_USE_DATE setting is deprecated, please use the "
        "IYPH_URLS_DATE_FORMAT setting with a value of 'year', 'month', "
        "or 'day'.")

register_setting(
    name="IYPH_URLS_DATE_FORMAT",
    label=_("Iyph post URL date format"),
    description=_("A string containing the value ``year``, ``month``, or "
        "``day``, which controls the granularity of the date portion in the "
        "URL for each iyph post. Eg: ``year`` will define URLs in the format "
        "/iyph/yyyy/slug/, while ``day`` will define URLs with the format "
        "/iyph/yyyy/mm/dd/slug/. An empty string means the URLs will only "
        "use the slug, and not contain any portion of the date at all."),
    editable=False,
    default=_IYPH_URLS_DATE_FORMAT,
)

register_setting(
    name="IYPH_POST_PER_PAGE",
    label=_("Iyph posts per page"),
    description=_("Number of iyph posts shown on a iyph listing page."),
    editable=True,
    default=5,
)

register_setting(
    name="IYPH_RSS_LIMIT",
    label=_("Iyph posts RSS limit"),
    description=_("Number of most recent iyph posts shown in the RSS feed. "
        "Set to ``None`` to display all iyph posts in the RSS feed."),
    editable=False,
    default=20,
)

register_setting(
    name="IYPH_SLUG",
    description=_("Slug of the page object for the iyph."),
    editable=False,
    default="iyph",
)
