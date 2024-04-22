"""
WSGI config for CN_Auction project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os, sys
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()




# =====================
# wsgi.py file begin 


# add the hellodjango project path into the sys.path
sys.path.append('CN_Auction\CN_Auction\hellodjango')

# add the virtualenv site-packages path to the sys.path
sys.path.append('vir_env\Lib\site-packages')

# poiting to the project settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CN_Auction.settings")

# wsgi.py file end
# ===================