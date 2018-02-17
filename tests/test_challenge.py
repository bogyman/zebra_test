import pytest


@pytest.mark.parametrize(
    'path,expected', (
        (['Buenos Aires', 'New York', 'Liverpool'], 10),
        (['Buenos Aires', 'Casablanca', 'Liverpool'], 8),
        (['Buenos Aires', 'Cape Town', 'New York', 'Liverpool', 'Casablanca'], 19),
        (['Buenos Aires', 'Cape Town', 'Casablanca'], 3),
        pytest.param(['Buenos Aires', 'Cape Town', 'Casablanca'], None, marks=pytest.mark.xfaixl),
    )
)
def test_total_journey_time(net_fixture, path, expected):
    res = net_fixture.get_total_journey_time(path)

    assert expected == res


