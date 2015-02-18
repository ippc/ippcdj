
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
settings_module = "%s.settings" % PROJECT_ROOT.split(os.sep)[-1]

# Add the app's directory to the PYTHONPATH
sys.path.append('/work/projects/ippcdj-env')
sys.path.append('/work/projects/ippcdj-env/ippcdj_repo')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
