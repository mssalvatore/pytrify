from collections.abc import MutableMapping, MutableSequence
from functools import lru_cache
from inspect import ismethod
from types import MappingProxyType
from typing import Type

from . import ListView

IMMUTABLE_TYPES = {  # using dict, not set, to preserve order
    bool: None,
    bytes: None,
    complex: None,
    float: None,
    frozenset: None,
    int: None,
    MappingProxyType: None,
    type(None): None,
    str: None,
    tuple: None,
}


class AccessError(TypeError):
    pass


def ro_init(self, obj):
    object.__setattr__(self, "_obj", obj)


def ro_sa(self, name, value):
    raise AccessError("Objects that are wrapped by a read-only wrapper do not support assignment")


def ro_ga(self, attr):
    attr_reference = getattr(object.__getattribute__(self, "_obj"), attr)

    if ismethod(attr_reference):
        return object.__getattribute__(self, attr)

    return wrap_object(attr_reference)


def wrap_object(obj: object):
    if type(obj) in IMMUTABLE_TYPES:
        return obj
    if isinstance(obj, MutableMapping):
        return to_mapping_proxy_type(obj)
    if isinstance(obj, MutableSequence):
        return to_immutable_sequence(obj)

    Wrapper = _create_wrapper_class(obj.__class__)  # ignore: type
    return Wrapper(obj)


@lru_cache(maxsize=None)
def _create_wrapper_class(class_: Type):
    return type(
        f"RO{class_.__name__}",
        (class_,),
        {"__init__": ro_init, "__setattr__": ro_sa, "__getattribute__": ro_ga},
    )


def to_immutable_sequence(sequence):
    return ListView(list(map(wrap_object, sequence)))


def to_mapping_proxy_type(mapping):
    return MappingProxyType({key: wrap_object(value) for key, value in mapping.items()})
