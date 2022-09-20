import os


from wsgi_static_middleware import StaticMiddleware

from simba_framework.main import Framework
from views import routes
from components.front_controllers import front_controllers

BASE_DIR = os.path.dirname(__name__)
STATIC_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]

# Создаем объект WSGI-приложения
application = Framework(routes, front_controllers)
app_static = StaticMiddleware(application,
                              static_root='staticfiles',
                              static_dirs=STATIC_DIRS)
