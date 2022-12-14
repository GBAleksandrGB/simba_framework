from quopri import decodestring

from components.routing import Router
from simba_framework.framework_requests import GetRequestClass


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:

    """Класс Framework - основа WSGI-фреймворка"""

    def __init__(self, routes_obj):
        self.request = {}
        self.routes_lst = routes_obj
        self.router = Router(self.request, self.routes_lst)

    def __call__(self, environ, start_response):
        # Получаем адрес, по которому пользователь выполнил переход
        path = environ['PATH_INFO']

        # Добавляем закрывающий слеш
        if not path.endswith('/'):
            path = f'{path}/'

        # Получаем все данные запроса
        method = environ['REQUEST_METHOD']
        self.request['method'] = method

        # обрабатываем запрос с помощью соотвествующего класса
        method_class = GetRequestClass(method)
        data = method_class.get_request_params(environ)
        self.request[method_class.dict_value] = Framework.decode_value(data)
        print(f'{method}: {Framework.decode_value(data)}')

        view = self.router.get_view(path, PageNotFound404())

        code, body = view(self.request)

        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
