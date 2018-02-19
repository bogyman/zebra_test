from collections import defaultdict
from typing import List, Dict, Tuple

from exceptions import BadRoadException


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
        self._cities: Dict[int, City] = {}
        self._cities_inverted_by_name: Dict[str, City] = {}
        self._courses: Dict[Tuple[City, City], Course] = {}
        self.graph: Dict[City, List[City]] = defaultdict(list)

    @property
    def cities_count(self) -> int:
        return len(self._cities)

    @property
    def cities(self) -> List[City]:
        return self._cities.values()

    def create_city(self, name: str) -> City:
        city = City(name)
        self._cities[city.pk] = city
        self._cities_inverted_by_name[city.name.lower()] = city

        return city

    def create_course(self, source: City, dest: City, distance: int) -> Course:
        if (source, dest) in self._courses:
            raise Exception('Course is already exist')

        course = Course(source, dest, distance)
        self.graph[source].append(course)
        self._courses[(source, dest)] = course

        return course

    def get_course(self, source: City, dest: City) -> Course:
        try:
            return self._courses[(source, dest)]
        except KeyError:
            raise BadRoadException()

    def get_city_by_name(self, city_name: str) -> City:
        return self._cities_inverted_by_name.get(city_name.lower())

    def get_adjacent_courses(self, city: City) -> List[Course]:
        return self.graph[city]
