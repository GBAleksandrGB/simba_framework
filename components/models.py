from quopri import decodestring
from sqlite3 import connect
from components.unit_of_work import DomainObject
from components.universal_mapper import BaseMapper


# Класс-Абстрактный пользователь
class User:
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs.get('name')

        if 'id' in kwargs:
            self.id = kwargs.get('id')


# Класс-Преподаватель
class Teacher(User):
    pass


# Класс-Студент
class Student(User, DomainObject):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if 'courses' in kwargs:
            self.courses = kwargs.get('courses')


# Класс-Фабрика пользователей
class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


# Класс-Курс
class Course(DomainObject):

    def __init__(self, **kwargs):

        if 'name' in kwargs:
            self.name = kwargs.get('name')

        if 'id' in kwargs:
            self.id = kwargs.get('id')

        if 'category' in kwargs:
            self.category = kwargs.get('category')


# Класс-Интерактивный курс
class InteractiveCourse(Course):
    pass


# Класс-Курс в записи
class RecordCourse(Course):
    pass


# Класс-Фабрика курсов
class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


# Класс-Категория
class Category(DomainObject):
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs.get('name')

        if 'id' in kwargs:
            self.id = kwargs.get('id')


# Класс-Основной интерфейс проекта
class Engine:

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category():
        return Category()

    @staticmethod
    def create_course(type_):
        return CourseFactory.create(type_)

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class StudentMapper(BaseMapper):
    tablename = 'students'
    model = Student


class CategoryMapper(BaseMapper):
    tablename = 'categories'
    model = Category


class CourseMapper(BaseMapper):
    tablename = 'courses'
    model = Course


connection = connect('project.sqlite')


class MapperRegistry:
    mappers = {
        'student': StudentMapper,
        'category': CategoryMapper,
        'course': CourseMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)
        elif isinstance(obj, Category):
            return CategoryMapper(connection)
        elif isinstance(obj, Course):
            return CourseMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)
