import pytest

from challenge import Challenge


@pytest.mark.parametrize(
    'path,expected', (
        (['Buenos Aires', 'New York', 'Liverpool'], 10),
        (['Buenos Aires', 'Casablanca', 'Liverpool'], 8),
        (['Buenos Aires', 'Cape Town', 'New York', 'Liverpool', 'Casablanca'], 19),
        pytest.param(['Buenos Aires', 'Cape Town', 'Casablanca'], None, marks=pytest.mark.xfail),
    )
)
def test_total_journey_time(net_fixture, path, expected):
    res = Challenge(net_fixture).get_total_journey_time(path)

    assert expected == res


@pytest.mark.parametrize(
    'source_name,dest_name,expected', (
        ('New York', 'Cape Town', 10),
        ('Buenos Aires', 'Liverpool', 8),
    )
)
def test_shortest_path(net_fixture, source_name, dest_name, expected):
    res = Challenge(net_fixture).get_shortest_path(source_name, dest_name)

    assert expected == res


@pytest.mark.parametrize(
    'source_name,dest_name,max_stops_count, expected', (
        ('Liverpool', 'Liverpool', 3, 2),
        ('Buenos Aires', 'Cape Town', 3, 4),
    )
)
def test_number_of_roads_less_3(net_fixture, source_name, dest_name, max_stops_count, expected):
    res = Challenge(net_fixture).get_number_of_roads(source_name, dest_name, max_stops_count)

    assert expected == res


@pytest.mark.parametrize(
    'source_name,dest_name,stops_count, expected', (
        ('Buenos Aires', 'Liverpool', 4, 3),
    )
)
def test_number_of_roads_4(net_fixture, source_name, dest_name, stops_count, expected):
    res = Challenge(net_fixture).get_number_of_roads(source_name, dest_name, stops_count)

    assert expected == res


@pytest.mark.parametrize(
    'source_name,dest_name,max_days, expected', (
        ('Liverpool', 'Liverpool', 25, 3),
    )
)
def test_number_of_roads_by_max_days(net_fixture, source_name, dest_name, max_days, expected):
    res = Challenge(net_fixture).get_number_of_roads_by_max_days(source_name, dest_name, max_days)

    assert expected == res
