from copy import copy
from itertools import zip_longest
from types import MappingProxyType

import pytest

from rowrapper import IMMUTABLE_TYPES, AccessError, ListView, wrap_object


class T:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.c = None

    def get_sum(self):
        return self.a + self.b

    def set_c(self, c):
        self.a = c


def test_get_attribute():
    obj = wrap_object(T(1, 2))

    assert obj.a == 1
    assert obj.b == 2


def test_immutible_attributes():
    obj = wrap_object(T(1, 2))

    with pytest.raises(AccessError):
        obj.a = 10
    with pytest.raises(AccessError):
        obj.b = 10


def test_method_calls():
    obj = wrap_object(T(1, 2))
    assert obj.get_sum() == 3


def test_method_call_cant_modify_object():
    obj = wrap_object(T(1, 2))
    with pytest.raises(AccessError):
        obj.set_c(3)


def test_wrapper_object_is_subclass():
    obj = wrap_object(T(None, None))
    assert isinstance(obj, T)


def test_modify_underlying_dict():
    test_dict = copy(TEST_DICT)
    obj = wrap_object(T(test_dict, None))

    assert "license_to_kill" not in obj.a
    test_dict["license_to_kill"] = True
    assert "license_to_kill" in obj.a


def test_modify_dict__depth_1():
    obj = wrap_object(T({"I": 1, "II": 2}, None))
    with pytest.raises(TypeError):
        obj.a["I"] = 10


def test_modify_dict__depth_2():
    test_dict = copy(TEST_DICT)
    obj = wrap_object(T({"agent": test_dict}, None))

    assert "license_to_kill" not in obj.a["agent"]
    test_dict["license_to_kill"] = True
    assert "license_to_kill" in obj.a["agent"]

    with pytest.raises(TypeError):
        obj.a["agent"]["cia_contact"] = "Felix Leiter"


def test_modify_dict_of_lists__depth_3():
    test_dict = copy(TEST_DICT)
    test_dict["equipment"] = ["Walther PPK", "Aston Martin"]
    obj = wrap_object(T({"agent": test_dict}, None))

    with pytest.raises(TypeError):
        obj.a["agent"]["equipment"].append("Rolex")


TEST_DICT = {"name": "bond, james bond", "designation": "007"}

IMMUTABLE_OBJECTS = [
    True,
    b"abc",
    complex(7, 144),
    3.14,
    frozenset((1, 2, 3)),
    42,
    MappingProxyType(TEST_DICT),
    None,
    "Hello, World!",
    (1, 2, 3),
]


@pytest.mark.parametrize("value,type_", zip_longest(IMMUTABLE_OBJECTS, IMMUTABLE_TYPES.keys()))
def test_immutable_types(value, type_):
    obj = wrap_object(T(value, None))
    assert isinstance(obj.a, type_)


def test_modify_list__depth_1():
    obj = wrap_object(T(["i", "ii", "iii", "iv"], None))
    with pytest.raises(TypeError):
        obj.a[2] = "x"

    with pytest.raises(TypeError):
        obj.a.append("x")

    assert isinstance(obj.a, ListView)


def test_modify_list__depth_2():
    a1 = [1, 2, 3]
    a2 = [4, 5, 6]
    a = [a1, a2]

    obj = wrap_object(T(a, None))

    assert len(obj.a[0]) == 3
    a1.append(3.5)
    assert len(obj.a[0]) == 4
    assert 3.5 in obj.a[0]

    assert len(obj.a) == 2
    assert isinstance(obj.a[0], ListView)
    assert isinstance(obj.a[1], ListView)

    with pytest.raises(TypeError):
        obj.a[1].append("x")


def test_modify_list_of_dicts__depth_3():
    test_dict = copy(TEST_DICT)
    a1 = [1, 2, 3]
    a2 = [4, 5, test_dict]
    a = [a1, a2]

    obj = wrap_object(T(a, None))
    assert "license_to_kill" not in obj.a[1][2]
    test_dict["license_to_kill"] = True
    assert "license_to_kill" in obj.a[1][2]

    with pytest.raises(TypeError):
        obj.a[1][2]["cia_contact"] = "Felix Leiter"