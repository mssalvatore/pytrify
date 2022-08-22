from copy import copy
from itertools import zip_longest
from types import MappingProxyType

import pytest

from pytrify import IMMUTABLE_TYPES, ImmutableAttributeError, ListView, pytrify


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
    obj = pytrify(T(1, 2))

    assert obj.a == 1
    assert obj.b == 2


def test_immutible_attributes():
    obj = pytrify(T(1, 2))

    with pytest.raises(ImmutableAttributeError):
        obj.a = 10
    with pytest.raises(ImmutableAttributeError):
        obj.b = 10


def test_method_calls():
    obj = pytrify(T(1, 2))
    assert obj.get_sum() == 3


def test_method_call_cant_modify_object():
    obj = pytrify(T(1, 2))
    with pytest.raises(ImmutableAttributeError):
        obj.set_c(3)


def test_wrapper_object_is_subclass():
    obj = pytrify(T(None, None))
    assert isinstance(obj, T)


def test_modify_underlying_dict():
    test_dict = copy(TEST_DICT)
    obj = pytrify(T(test_dict, None))

    assert "license_to_kill" not in obj.a
    test_dict["license_to_kill"] = True
    assert "license_to_kill" in obj.a


def test_modify_dict__depth_1():
    obj = pytrify(T({"I": 1, "II": 2}, None))
    with pytest.raises(TypeError):
        obj.a["I"] = 10


def test_modify_dict__depth_2():
    test_dict = copy(TEST_DICT)
    obj = pytrify(T({"agent": test_dict}, None))

    assert "license_to_kill" not in obj.a["agent"]
    test_dict["license_to_kill"] = True
    assert "license_to_kill" in obj.a["agent"]

    with pytest.raises(TypeError):
        obj.a["agent"]["cia_contact"] = "Felix Leiter"


def test_modify_dict_of_lists__depth_3():
    test_dict = copy(TEST_DICT)
    test_dict["equipment"] = ["Walther PPK", "Aston Martin"]
    obj = pytrify(T({"agent": test_dict}, None))

    with pytest.raises(TypeError):
        obj.a["agent"]["equipment"].append("Rolex")


TEST_DICT = {"name": "bond, james bond", "designation": "007"}

IMMUTABLE_OBJECTS = [
    True,
    b"abc",
    complex(7, 144),
    3.14,
    42,
    None,
    "Hello, World!",
    range(0, 10),
]


@pytest.mark.parametrize("value,type_", zip_longest(IMMUTABLE_OBJECTS, IMMUTABLE_TYPES.keys()))
def test_immutable_types(value, type_):
    obj = pytrify(T(value, None))
    assert isinstance(obj.a, type_)


def test_modify_list__depth_1():
    obj = pytrify(T(["i", "ii", "iii", "iv"], None))
    with pytest.raises(TypeError):
        obj.a[2] = "x"

    with pytest.raises(TypeError):
        obj.a.append("x")

    assert isinstance(obj.a, ListView)


def test_modify_list__depth_2():
    a1 = [1, 2, 3]
    a2 = [4, 5, 6]
    a = [a1, a2]

    obj = pytrify(T(a, None))

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

    obj = pytrify(T(a, None))
    assert "license_to_kill" not in obj.a[1][2]
    test_dict["license_to_kill"] = True
    assert "license_to_kill" in obj.a[1][2]

    with pytest.raises(TypeError):
        obj.a[1][2]["cia_contact"] = "Felix Leiter"


def test_modify_mapping_keys():
    t = T(1, 2)

    d = pytrify({t: "value"})

    with pytest.raises(ImmutableAttributeError):
        for key in d.keys():
            key.a = 12345


def test_modify_mapping_proxy_type_value():
    mpt = pytrify(MappingProxyType({"test": T(1, 2)}))

    with pytest.raises(ImmutableAttributeError):
        mpt["test"].a = 12345


@pytest.mark.parametrize("test_set", [set([T(1, 2)]), frozenset([T(1, 2)])])
def test_modify_set_item(test_set):
    immutable_set = pytrify(test_set)

    with pytest.raises(ImmutableAttributeError):
        for item in immutable_set:
            item.a = 12345


def test_modify_tuple_element():
    pytrified_tuple = pytrify((T(1, 2), T(3, 4), T(5, 6)))

    with pytest.raises(ImmutableAttributeError):
        pytrified_tuple[0].a = 1

    with pytest.raises(ImmutableAttributeError):
        pytrified_tuple[1].a = 1

    with pytest.raises(ImmutableAttributeError):
        pytrified_tuple[2].a = 1
