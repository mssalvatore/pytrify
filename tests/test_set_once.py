import pytest

from pytrify import ImmutableAttributeError, SetOnce


class T:
    member = SetOnce()


def test_set_once():
    t = T()
    t.member = 1
    with pytest.raises(ImmutableAttributeError):
        t.member = 2


def test_set_once__different_objects():
    t1 = T()
    t2 = T()

    # Raises exception on failure
    t1.member = 1
    t2.member = 1
