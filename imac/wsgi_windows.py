import os
print("wsgi_windows.py")
import sys

import site

from django.core.wsgi import get_wsgi_application

# Add the app’s directory to the PYTHONPATH

sys.path.append("D:/MyCode/MainProjects/iman-main/imac")

sys.path.append("D:/MyCode/MainProjects/iman-main/imac/imac")

os.environ["DJANGO_SETTINGS_MODULE"] = "imac.settings"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "imac.settings")

application = get_wsgi_application()

