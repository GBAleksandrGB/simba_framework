from datetime import date
from jsonpickle import dumps, loads

from components.models import Engine, MapperRegistry
from components.decorators import AppRoute
from components.cbv import ListView, CreateView, TemplateView
from components.unit_of_work import UnitOfWork

site = Engine()
routes = {}
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


# Класс-контроллер - Главная страница
@AppRoute(routes=routes, url='/')
class Index(TemplateView):
    template_name = 'index.html'


# Класс-контроллер - Страница "О проекте"
@AppRoute(routes=routes, url='/about/')
class About(TemplateView):
    template_name = 'about.html'


# Класс-контроллер - Страница "Расписания"
@AppRoute(routes=routes, url='/study_programs/')
class StudyPrograms(TemplateView):
    template_name = 'study-programs.html'

    def get_context_data(self, request):
        context = super().get_context_data(request)
        context['data'] = date.today().strftime('%d-%m-%Y')
        return context


# Класс-контроллер - Страница 404
class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# Класс-контроллер - Страница "Список курсов"
@AppRoute(routes=routes, url='/courses_list/')
class CoursesList(ListView):
    template_name = 'courses-list.html'

    def get_queryset(self, request):
        courses = MapperRegistry.get_current_mapper('course').all()
        courses_lst = []
        category = MapperRegistry.get_current_mapper('category').get_by_category_id(request['get_params']['id'])

        for course in courses:
            if course.category == category.name:
                courses_lst.append(course)
        return courses_lst

    def get_context_data(self, request):
        context = super().get_context_data(request)
        category = MapperRegistry.get_current_mapper('category').get_by_category_id(request['get_params']['id'])
        context['name'] = category.name
        context['id'] = category.id
        return context


# Класс-контроллер - Страница "Создать курс"
@AppRoute(routes=routes, url='/create_course/')
class CourseCreateView(CreateView):
    template_name = 'create-course.html'

    def get_context_data(self, request):
        context = super().get_context_data(request)
        categories = MapperRegistry.get_current_mapper('category').all()
        context['categories'] = categories
        return context

    def create_obj(self, data: dict):

        try:
            name = data.get('name')
            if name == '':
                raise ValueError
        except ValueError:
            pass
        else:
            name = site.decode_value(name)

            try:
                category = data.get('category')
                if category == 'Выберите категорию':
                    raise ValueError
            except ValueError:
                pass
            else:
                category = site.decode_value(category)
                new_category = site.create_course('record')
                schema = {'name': name, 'category': category}
                new_category.mark_new(schema)
                UnitOfWork.get_current().commit()


# Класс-контроллер - Страница "Создать категорию"
@AppRoute(routes=routes, url='/create_category/')
class CategoryCreateView(CreateView):
    template_name = 'create-category.html'

    def create_obj(self, data: dict):
        try:
            name = data.get('name')
            if name == '':
                raise ValueError
        except ValueError:
            pass
        else:
            name = site.decode_value(name)
            new_category = site.create_category()
            schema = {'name': name}
            new_category.mark_new(schema)
            UnitOfWork.get_current().commit()


# Класс-контроллер - Страница "Список категорий"
@AppRoute(routes=routes, url='/category_list/')
class CategoryListView(ListView):
    template_name = 'category-list.html'

    def get_queryset(self, request):
        categories = MapperRegistry.get_current_mapper('category').all()
        return categories


@AppRoute(routes=routes, url='/student_list/')
class StudentListView(ListView):
    template_name = 'student-list.html'

    def get_queryset(self, request):
        students = MapperRegistry.get_current_mapper('student').all()
        return students


@AppRoute(routes=routes, url='/create_student/')
class StudentCreateView(CreateView):
    template_name = 'create-student.html'

    def create_obj(self, data: dict):
        try:
            name = data.get('name')
            if name == '':
                raise ValueError
        except ValueError:
            pass
        else:
            name = site.decode_value(name)
            new_obj = site.create_user('student')
            schema = {'name': name}
            new_obj.mark_new(schema)
            UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/add_student/')
class AddStudentByCourseView(CreateView):
    template_name = 'add-student.html'

    def get_context_data(self, request):
        context = super().get_context_data(request)
        context['courses'] = MapperRegistry.get_current_mapper('course').all()
        context['students'] = MapperRegistry.get_current_mapper('student').all()
        return context

    def create_obj(self, data: dict):
        try:
            student_id = data['student_id']
            if student_id == 'Выберите студента':
                raise ValueError
        except ValueError:
            pass
        else:
            student = MapperRegistry.get_current_mapper('student').get_by_student_id(student_id)

            try:
                course = data['course']
                if course == 'Выберите курс':
                    raise ValueError
            except ValueError:
                pass
            else:
                course = site.decode_value(course)
                student_courses = student.courses
                student_courses = [] if student_courses is None else [student_courses]
                student_courses.append(course)
                schema = {'courses': ', '.join(student_courses)}
                student.mark_dirty(schema)
                UnitOfWork.get_current().commit()


class BaseSerializer:
    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)


@AppRoute(routes=routes, url='/api/<cat>/')
class CourseApi:
    def __call__(self, request):
        cat_id = request.get('url_vars').get('cat')
        cat = MapperRegistry.get_current_mapper('category').get_by_category_id(int(cat_id))
        return '200 OK', BaseSerializer(cat).save()
