from simba_framework.templator import render


# Класс-контроллер для простейшего рендеринга HTML-шаблонов
class TemplateView:
    template_name = 'template.html'

    def get_context_data(self, request):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self, request):
        template_name = self.get_template()
        context = self.get_context_data(request)
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context(request)


# Класс-контроллер для отображения списков записей
class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self, request):
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self, request):
        queryset = self.get_queryset(request)
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


# Класс-контроллер для создания записи
class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):

        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_obj(data)
            return self.render_template_with_context(request)
        else:
            return super().__call__(request)
