import models


def test_pkmeta():
    c1 = models.City('name2')
    c2 = models.City('name3')

    assert c1.pk == 1
    assert c2.pk == 2
