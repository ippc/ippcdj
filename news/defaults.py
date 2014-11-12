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
    name="NEWS_USE_FEATURED_IMAGE",
    description=_("Enable featured images in news posts"),
    editable=False,
    default=False,
)

_NEWS_URLS_DATE_FORMAT = ""
if getattr(settings, "NEWS_URLS_USE_DATE", False):
    _NEWS_URLS_DATE_FORMAT = "day"
    from warnings import warn
    warn("NEWS_URLS_USE_DATE setting is deprecated, please use the "
        "NEWS_URLS_DATE_FORMAT setting with a value of 'year', 'month', "
        "or 'day'.")

register_setting(
    name="NEWS_URLS_DATE_FORMAT",
    label=_("News post URL date format"),
    description=_("A string containing the value ``year``, ``month``, or "
        "``day``, which controls the granularity of the date portion in the "
        "URL for each news post. Eg: ``year`` will define URLs in the format "
        "/news/yyyy/slug/, while ``day`` will define URLs with the format "
        "/news/yyyy/mm/dd/slug/. An empty string means the URLs will only "
        "use the slug, and not contain any portion of the date at all."),
    editable=False,
    default=_NEWS_URLS_DATE_FORMAT,
)

register_setting(
    name="NEWS_POST_PER_PAGE",
    label=_("Bews posts per page"),
    description=_("Number of news posts shown on a news listing page."),
    editable=True,
    default=5,
)

register_setting(
    name="NEWS_RSS_LIMIT",
    label=_("Bews posts RSS limit"),
    description=_("Number of most recent news posts shown in the RSS feed. "
        "Set to ``None`` to display all news posts in the RSS feed."),
    editable=False,
    default=20,
)

register_setting(
    name="NEWS_SLUG",
    description=_("Slug of the page object for the news."),
    editable=False,
    default="news",
)
