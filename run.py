import os
# from wsgiref.simple_server import make_server

import wsgi_static_middleware

from simba_framework.main import Framework
from views import routes

BASE_DIR = os.path.dirname(__name__)
STATIC_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]

# Создаем объект WSGI-приложения
application = Framework(routes)
app_static = wsgi_static_middleware.StaticMiddleware(application,
                                                     static_root='staticfiles',
                                                     static_dirs=STATIC_DIRS)

# with make_server('', 8080, app_static) as httpd:
#     print("Запуск на порту 8080...")
#     httpd.serve_forever()
