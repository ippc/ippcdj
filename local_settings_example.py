
DEBUG = True

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.mysql",
        # DB name or path to database file if using sqlite3.
        "NAME": "ippc_django_new",
        # Not used with sqlite3.
        "USER": "root",
        # Not used with sqlite3.
        "PASSWORD": "somesecretpassword",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ""

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = ""

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ""

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = ""


ALLOWED_HOSTS = ["subdomain.domain.tld"]
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
ENVELOPE_EMAIL_RECIPIENTS=["name@email.tld"]
SECRET_KEY = "somethingsecretdonotshare!"