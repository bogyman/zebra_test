import pytest

import models


@pytest.fixture
def net_fixture():
    net = models.Net()

    new_york = net.create_city('New York')
    liverpool = net.create_city('Liverpool')
    buenos_aires = net.create_city('Buenos Aires')
    cape_town = net.create_city('Cape Town')
    casablanca = net.create_city('Casablanca')

    # kyiv = net.create_city('Kyiv')
    # tokio = net.create_city('Tokio')

    net.create_course(buenos_aires, new_york, 6)
    net.create_course(buenos_aires, casablanca, 5)
    net.create_course(buenos_aires, cape_town, 4)
    net.create_course(new_york, liverpool, 4)
    net.create_course(liverpool, casablanca, 3)
    net.create_course(liverpool, cape_town, 6)
    net.create_course(casablanca, liverpool, 3)
    net.create_course(casablanca, cape_town, 6)
    net.create_course(cape_town, new_york, 8)

    # net.create_course(kyiv, tokio, 8)
    # net.create_course(casablanca, kyiv, 7)
    # net.create_course(tokio, liverpool, 7)
    # net.create_course(tokio, casablanca, 7)

    return net
