from collections import defaultdict
from typing import List


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
        self._cities = {}
        self._cities_inverted_by_name = {}
        self._courses = {}
        self._graph = defaultdict(list)

    def create_city(self, name: str):
        city = City(name)
        self._cities[city.pk] = city
        self._cities_inverted_by_name[city.name.lower()] = city

        return city

    def create_course(self, source: City, dest: City, distance: int):
        if (source, dest) in self._courses:
            raise Exception('Course is already exist')

        course = Course(source, dest, distance)
        self._graph[source].append(course)
        self._courses[(source, dest)] = course

        return course

    def get_course(self, source: City, dest: City):
        return self._courses[(source, dest)]

    def get_city_by_name(self, city_name: str):
        return self._cities_inverted_by_name.get(city_name.lower())

    def get_total_journey_time(self, path: List[str]):
        cities = [self.get_city_by_name(city_name) for city_name in path]
        source_dest_list = ((cities[i-1], cities[i])for i in range(1, len(cities)))

        try:
            return sum((self.get_course(source, dest).distance for source, dest in source_dest_list))
        except KeyError:
            raise Exception('Path is invalid')


