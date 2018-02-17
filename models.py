from collections import defaultdict


class PkMeta(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls._pk = 1


class PkBase(metaclass=PkMeta):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.pk = cls._pk
        cls._pk += 1

        return instance


class City(PkBase):
    def __init__(self, name: str):
        self.name = name


class Course(PkBase):
    def __init__(self, source: City, dest: City, distance: int):
        self.source = source
        self.dest = dest
        self.distance = distance


class Net(PkBase):
    def __init__(self):
        self.cities = {}
        self.distances = {}
        self.courses = {}
        self.graph = defaultdict(list)

    def create_city(self, name: str):
        city = City(name)
        self.cities[city.pk] = city

        return city

    def create_course(self, source: City, dest: City, distance: int):
        course = Course(source, dest, distance)
        self.graph[source].append(course)
        return course

