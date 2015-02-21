# -*- coding: utf-8 -*-
######################
# MEZZANINE SETTINGS #
######################

# The following settings are already defined with default values in
# the ``defaults.py`` module within each of Mezzanine's apps, but are
# common enough to be put here, commented out, for convenient
# overriding. Please consult the settings documentation for a full list
# of settings Mezzanine implements:
# http://mezzanine.jupo.org/docs/configuration.html#default-settings

# Controls the ordering and grouping of the admin menu.
#
# ADMIN_MENU_ORDER = (
#     ("Content", ("pages.Page", "blog.BlogPost",
#        "generic.ThreadedComment", ("Media Library", "fb_browse"),)),
#     ("Site", ("sites.Site", "redirects.Redirect", "conf.Setting")),
#     ("Users", ("auth.User", "auth.Group",)),
# )

# A three item sequence, each containing a sequence of template tags
# used to render the admin dashboard.
#
# DASHBOARD_TAGS = (
#     ("blog_tags.quick_blog", "mezzanine_tags.app_list"),
#     ("comment_tags.recent_comments",),
#     ("mezzanine_tags.recent_actions",),
# )

# A sequence of templates used by the ``page_menu`` template tag. Each
# item in the sequence is a three item sequence, containing a unique ID
# for the template, a label for the template, and the template path.
# These templates are then available for selection when editing which
# menus a page should appear in. Note that if a menu template is used
# that doesn't appear in this setting, all pages will appear in it.

# PAGE_MENU_TEMPLATES = (
#     (1, "Top navigation bar", "pages/menus/dropdown.html"),
#     (2, "Left-hand tree", "pages/menus/tree.html"),
#     (3, "Footer", "pages/menus/footer.html"),
# )

# A sequence of fields that will be injected into Mezzanine's (or any
# library's) models. Each item in the sequence is a four item sequence.
# The first two items are the dotted path to the model and its field
# name to be added, and the dotted path to the field class to use for
# the field. The third and fourth items are a sequence of positional
# args and a dictionary of keyword args, to use when creating the
# field instance. When specifying the field class, the path
# ``django.models.db.`` can be omitted for regular Django model fields.
#
# EXTRA_MODEL_FIELDS = (
#     (
#         # Dotted path to field.
#         "mezzanine.blog.models.BlogPost.image",
#         # Dotted path to field class.
#         "somelib.fields.ImageField",
#         # Positional args for field class.
#         ("Image",),
#         # Keyword args for field class.
#         {"blank": True, "upload_to": "blog"},
#     ),
#     # Example of adding a field to *all* of Mezzanine's content types:
#     (
#         "mezzanine.pages.models.Page.another_field",
#         "IntegerField", # 'django.db.models.' is implied if path is omitted.
#         ("Another name",),
#         {"blank": True, "default": 1},
#     ),
# )

# Setting to turn on featured images for blog posts. Defaults to False.
#
BLOG_USE_FEATURED_IMAGE = True
CALLS_USE_FEATURED_IMAGE = True
NEWS_USE_FEATURED_IMAGE = True

# If True, the south application will be automatically added to the
# INSTALLED_APPS setting.
USE_SOUTH = True

PAGE_MENU_TEMPLATES_DEFAULT = [2]
########################
# MAIN DJANGO SETTINGS #
########################

# People who get code error notifications.
# In the format (('Full Name', 'email@example.com'),
#                ('Full Name', 'anotheremail@example.com'))
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = None

# If you set this to True, Django will use timezone-aware datetimes.
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en"

# A boolean that turns on/off debug mode. When set to ``True``, stack traces
# are displayed for error pages. Should always be set to ``False`` in
# production. Best set to ``True`` in local_settings.py
DEBUG = False

# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Tuple of IP addresses, as strings, that:
#   * See debug comments, when DEBUG is true
#   * Receive x-headers
INTERNAL_IPS = ("127.0.0.1",)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

AUTHENTICATION_BACKENDS = (
    "mezzanine.core.auth_backends.MezzanineBackend",
    "guardian.backends.ObjectPermissionBackend",
)

ANONYMOUS_USER_ID = -1

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.DefaultStorageFinder",
)

# The numeric mode to set newly-uploaded files to. The value should be
# a mode you'd pass directly to os.chmod.
FILE_UPLOAD_PERMISSIONS = 0644


#############
# DATABASES #
#############

DATABASES = {
    "default": {
        # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.",
        # DB name or path to database file if using sqlite3.
        "NAME": "",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}


#########
# PATHS #
#########

import os

# Full filesystem path to the project.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Name of the directory for the project.
PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_DIRNAME

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = STATIC_URL + "media/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))

# Package/module name to import the root urlpatterns from for the project.
ROOT_URLCONF = "%s.urls" % PROJECT_DIRNAME

# Put strings here, like "/home/html/django_templates"
# or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, "templates"),)


################
# APPLICATIONS #
################

INSTALLED_APPS = (
    
    # /en/, /es/ etc in urls
    "localeurl",
    "autocomplete_light",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",

    # ippc theme
    "ippc",
    
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
    "mezzanine.blog",
    "mezzanine.forms",
    "mezzanine.pages",
    "mezzanine.galleries",
    "mezzanine.twitter",
    
    # enabling user accounts
    "mezzanine.accounts",
    
    # countries for user accounts
    "django_countries",
    
    # markdown wysiwyg editor
    "mezzanine_pagedown",
    
    # file collections for publications
    "mezzanine_file_collections",

    # forum application, based on mezzanine.blog
    "forum",
    "calls",
    "news",

    # or, even better, attachments that can be related to any model type
    
    # https://github.com/bartTC/django-attachments
    # "attachments",
    
    # https://github.com/Alem/django-jfu
    # "jfu",
    
    # south for database data migrations
    "south",
    
    # guardian for view permissions
    "guardian",
    
    # for email utility
    # http://stackoverflow.com/a/1823193/412329

    "leaflet",
    # debug toolbar
    # "debug_toolbar",
    
    #"mezzanine.mobile",
    "schedule",
    "django_markdown",
    "envelope"

)

# NEWSLETTER_CONFIRM_EMAIL = False

# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.static",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.tz",
    "mezzanine.conf.context_processors.settings",
)

# List of middleware classes to use. Order is important; in the request phase,
# these middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE_CLASSES = (
    
    # debug toolbar
    # "debug_toolbar.middleware.DebugToolbarMiddleware",

    "mezzanine.core.middleware.UpdateCacheMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    
    # localization for multi-lingual site
    # http://www.djangobook.com/en/2.0/chapter19.html
    "django.middleware.locale.LocaleMiddleware",
    # https://bitbucket.org/carljm/django-localeurl/src/764caf7a412d77aca8cc929988f333ee808719e6/docs/setup.rst?at=default
    "localeurl.middleware.LocaleURLMiddleware",
    
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "mezzanine.core.request.CurrentRequestMiddleware",
    "mezzanine.core.middleware.RedirectFallbackMiddleware",
    "mezzanine.core.middleware.TemplateForDeviceMiddleware",
    "mezzanine.core.middleware.TemplateForHostMiddleware",
    "mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware",
    "mezzanine.core.middleware.SitePermissionMiddleware",
    # Uncomment the following if using any of the SSL settings:
    # "mezzanine.core.middleware.SSLRedirectMiddleware",
    "mezzanine.pages.middleware.PageMiddleware",
    "mezzanine.core.middleware.FetchFromCacheMiddleware",
)

LANGUAGE_CODE == 'en'
# https://docs.djangoproject.com/en/1.3/ref/settings/#std:setting-LANGUAGES
# http://pythonhosted.org/django-localeurl/usage.html

# ugettext = lambda s: s
# LANGUAGES = (
#    ('en', ugettext('English')),
#    ('fr', ugettext('French')),
#    ('es', ugettext('Spanish')),
#    ('ru', ugettext('Russian')),
#    ('ar', ugettext('Arabic')),
#    ('zh', ugettext('Chinese')),
# )

# https://docs.djangoproject.com/en/1.5/ref/settings/#std:setting-LANGUAGES
from django.utils.translation import ugettext_lazy as _

LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
    ('es', _('Spanish')),
    ('ru', _('Russian')),
    ('ar', _('Arabic')),
    ('zh', _('Chinese')),

)

# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = (os.path.join(PROJECT_ROOT, "conf/locale"),)

SEARCH_MODEL_CHOICES = ("pages.Page", "news.NewsPost","calls.CallsPost","ippc.Publication", "ippc.ReportingObligation","ippc.EventReporting","ippc.PestReport")
CALLS_SLUG = 'calls'
NEWS_SLUG = 'news'
# BLOG_SLUG = 'news'
#CALLS_USE_FEATURED_IMAGE = 'True'
FORUM_SLUG = 'forum'
# FORUM_USE_FEATURED_IMAGE = 'True'
# FORUM_URLS_DATE_FORMAT = 'month'
COMMENTS_USE_RATINGS = False
SITE_TITLE = _("International Plant Protection Convention")
SITE_TAGLINE = _("Protecting the world's plant resources from pests")

AUTH_PROFILE_MODULE = "ippc.IppcUserProfile"
ACCOUNTS_PROFILE_VIEWS_ENABLED = True
ACCOUNTS_MIN_PASSWORD_LENGTH = 8
ACCOUNTS_VERIFICATION_REQUIRED = True
# ACCOUNTS_APPROVAL_REQUIRED = False
# ACCOUNTS_APPROVAL_EMAILS = 'simon.griffee@fao.org, paola.sentinelli@fao.org'
   
ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS = (
#    "user",
    "username",
#    "first_name",
#    "last_name",
    "gender",
    "title",
    "contact_type",
    "address_country",
    "city",
    "state",
    "zipcode",
    "country",
    "partner",
    "date_account_created",
    "preferredlanguage",
)


ALLOWED_HOSTS = ["127.0.0.1:8000"]

RICHTEXT_WIDGET_CLASS = 'mezzanine_pagedown.widgets.PageDownWidget'
# RICHTEXT_WIDGET_CLASS = 'mezzanine.core.forms.TinyMceWidget'
RICHTEXT_FILTER = 'mezzanine_pagedown.filters.custom'
RICHTEXT_FILTER_LEVEL = 3
PAGEDOWN_MARKDOWN_EXTENSIONS = ('extra','codehilite','toc')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#EMAIL_USE_TLS = True
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_HOST_USER = 'xxx@gmail.com'
#EMAIL_HOST_PASSWORD = 'xxx'
#DEFAULT_FROM_EMAIL='xxx@gmail.com'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
#EMAIL_USE_TLS = True

ENVELOPE_EMAIL_RECIPIENTS=['paola.sentinelli@fao.org']

ENVELOPE_CONTACT_CHOICES = (
    (10,    _("Secretariat")),
    (None,  _("Website feedback")),
)



# http://codespatter.com/2009/04/10/how-to-add-locations-to-python-path-for-reusable-django-apps/
# import sys
# sys.path.insert(0, os.path.join(PROJECT_ROOT, "apps"))



# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"

# GRAPPELLI_ADMIN_HEADLINE = ""
GRAPPELLI_ADMIN_TITLE = "IPPC Administration - click to view site"

#########################
# OPTIONAL APPLICATIONS #
#########################

# These will be added to ``INSTALLED_APPS``, only if available.
OPTIONAL_APPS = (
    # "debug_toolbar",
    "django_extensions",
    "compressor",
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TEMPLATE_CONTEXT': True,
    'INTERCEPT_REDIRECTS': False,
}

###################
# DEPLOY SETTINGS #
###################

# These settings are used by the default fabfile.py provided.
# Check fabfile.py for defaults.

# FABRIC = {
#     "SSH_USER": "", # SSH username
#     "SSH_PASS":  "", # SSH password (consider key-based authentication)
#     "SSH_KEY_PATH":  "", # Local path to SSH key file, for key-based auth
#     "HOSTS": [], # List of hosts to deploy to
#     "VIRTUALENV_HOME":  "", # Absolute remote path for virtualenvs
#     "PROJECT_NAME": "", # Unique identifier for project
#     "REQUIREMENTS_PATH": "", # Path to pip requirements, relative to project
#     "GUNICORN_PORT": 8000, # Port gunicorn will listen on
#     "LOCALE": "en_US.UTF-8", # Should end with ".UTF-8"
#     "LIVE_HOSTNAME": "www.example.com", # Host for public site.
#     "REPO_URL": "", # Git or Mercurial remote repo URL for the project
#     "DB_PASS": "", # Live database password
#     "ADMIN_PASS": "", # Live admin user password
# }


##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.
try:
    from local_settings import *
except ImportError:
    pass


####################
# DYNAMIC SETTINGS #
####################

# set_dynamic_settings() will rewrite globals based on what has been
# defined so far, in order to provide some better defaults where
# applicable. We also allow this settings module to be imported
# without Mezzanine installed, as the case may be when using the
# fabfile, where setting the dynamic settings below isn't strictly
# required.
try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())
