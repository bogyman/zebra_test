from zebra_app import models


def test_pkmeta():
    c1 = models.City('name2')
    c2 = models.City('name3')

    assert c2.pk == c1.pk + 1
