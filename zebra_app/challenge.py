from collections import defaultdict
from typing import List

from zebra_app.exceptions import BadRoadException
from zebra_app.models import Net, City


class Challenge:
    def __init__(self, net: Net):
        self.net = net

    def get_total_journey_time(self, path: List[str]) -> int:
        """

        :param path: List of city names
        :return: int
        """
        cities = [self.net.get_city_by_name(city_name) for city_name in path]
        source_dest_list = ((cities[i - 1], cities[i]) for i in range(1, len(cities)))

        return sum((self.net.get_course(source, dest).distance for source, dest in source_dest_list))

    def get_shortest_path(self, source_name: str, dest_name: str) -> int:
        """
        Using Dijkstra’s shortest path algorithm
        :param source_name:
        :param dest_name:
        :return: int
        """
        source_city = self.net.get_city_by_name(source_name)
        dest_city = self.net.get_city_by_name(dest_name)

        spt_set = set()
        dist = {source_city: 0}

        for ____ in range(self.net.cities_count):
            # get city with min dist to source that is not in spt_set
            # x[0] - city
            # x[1] - distance
            current_city, current_distance = min(
                filter(lambda x: x[0] not in spt_set, dist.items()),
                default=(None, None),
                key=lambda x: x[1]
            )

            if not current_city:
                raise Exception('Path is invalid')

            if current_city == dest_city:
                return current_distance

            spt_set.add(current_city)

            for course in self.net.get_adjacent_courses(current_city):
                if course.dest in spt_set:
                    continue

                should_update_dist = (
                    not dist.get(course.dest)
                    or (dist.get(course.dest) and dist[course.dest] > current_distance + course.distance)
                )

                if should_update_dist:
                    dist[course.dest] = current_distance + course.distance

    def _get_number_of_roads_less_3(self, city: City, dest_city: City, stops_count: int) -> int:
        """

        :param city:
        :param dest_city:
        :param stops_count:
        :return:
        """
        count = 0
        if stops_count == 0 and city == dest_city:
            return 1

        if stops_count <= 0:
            return 0

        for course in self.net.get_adjacent_courses(city):
            if course.dest == dest_city:
                return count + 1
            else:
                count += self._get_number_of_roads_less_3(course.dest, dest_city, stops_count - 1)

        return count

    def _get_number_of_roads_more_3(self, source_city: City, dest_city: City, stops_count: int) -> int:
        """
        used algoritm from https://www.geeksforgeeks.org/count-possible-paths-source-destination-exactly-k-edges/
        :param source_city:
        :param dest_city:
        :param stops_count:
        :return:
        """
        count = defaultdict(lambda: defaultdict(lambda: [0] * (stops_count+1)))

        for stops_count_ in range(stops_count+1):
            for _source_city in self.net.cities:
                for _dest_city in self.net.cities:
                    if stops_count_ == 0 and _source_city == _dest_city:
                        count[_source_city][_dest_city][stops_count_] = 1

                    try:
                        course = self.net.get_course(_source_city, _dest_city)
                    except BadRoadException:
                        course = None

                    if stops_count_ == 1 and course:
                        count[_source_city][_dest_city][stops_count_] = 1

                    if stops_count_ > 1:
                        for course in self.net.get_adjacent_courses(_source_city):
                            count[_source_city][_dest_city][stops_count_] += count[course.dest][_dest_city][stops_count_ - 1]

        return count[source_city][dest_city][stops_count]

    def get_number_of_roads(self, source_name: str, dest_name: str, max_stops_count: int) -> int:
        """

        :param source_name:
        :param dest_name:
        :param max_stops_count:
        :return:
        """
        source_city = self.net.get_city_by_name(source_name)
        dest_city = self.net.get_city_by_name(dest_name)

        if max_stops_count > 3:
            return self._get_number_of_roads_more_3(source_city, dest_city, max_stops_count)
        else:
            return self._get_number_of_roads_less_3(source_city, dest_city, max_stops_count)

    def _get_number_of_roads_by_days(self, city: City, dest_city: City, max_days: int, road_days: int) -> int:
        """

        :param city:
        :param dest_city:
        :param max_days:
        :param road_days:
        :return:
        """
        count = 0
        if road_days > max_days:
            return 0

        if road_days > 0 and city == dest_city:
            return 1

        for course in self.net.get_adjacent_courses(city):
            count += self._get_number_of_roads_by_days(course.dest, dest_city, max_days, road_days+course.distance)

        return count

    def get_number_of_roads_by_max_days(self, source_name: str, dest_name: str, max_days: int) -> int:
        """

        :param source_name:
        :param dest_name:
        :param max_days:
        :return:
        """
        source_city = self.net.get_city_by_name(source_name)
        dest_city = self.net.get_city_by_name(dest_name)

        return self._get_number_of_roads_by_days(source_city, dest_city, max_days, 0)
