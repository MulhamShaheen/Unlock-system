import os
import sys
import platform

# путь к проекту, там где manage.py
sys.path.insert(0, '/home/c/cw65021/unlock/public_html/unlock')
# путь к фреймворку, там где settings.py
sys.path.insert(0, '/home/c/cw65021/unlock/public_html/unlock/unlock')
# путь к виртуальному окружению myenv
sys.path.insert(0, '/home/c/cw65021/unlock/venv/lib/python3.6/site-packages')
# sys.path.insert(0, '/home/c/cx53558/newsite/myenv/lib/python3.6/site-packages')
os.environ["DJANGO_SETTINGS_MODULE"] = "unlock.settings"

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
