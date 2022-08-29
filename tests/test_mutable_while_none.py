import pytest

from pytrify import ImmutableAttributeError, MutableWhileNone


class T:
    member = MutableWhileNone()


def test_mutable_while_none__none_by_default():
    t = T()
    assert t.member is None


def test_mutable_while_none__get_member():
    t = T()

    t.member = 1
    assert t.member == 1


def test_mutable_while_none__raises_on_reset():
    t = T()
    t.member = 1

    with pytest.raises(ImmutableAttributeError):
        t.member = 2


def test_mutable_while_none__set_to_none():
    t = T()

    t.member = None
    # Raises exception on failure
    t.member = None


def test_immutable_attribute_error_message():
    t = T()
    t.member = 1

    with pytest.raises(ImmutableAttributeError) as err:
        t.member = 2

    assert "T.member" in str(err.value)
