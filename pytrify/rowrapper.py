from collections.abc import MutableMapping, MutableSequence
from functools import lru_cache
from inspect import ismethod
from types import MappingProxyType
from typing import Type

from . import ImmutableAttributeError, ListView

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


def wrap_readonly(obj: object):
    if type(obj) in IMMUTABLE_TYPES:
        return obj

    if isinstance(obj, MutableMapping):
        return to_mapping_proxy_type(obj)

    if isinstance(obj, MutableSequence):
        return to_immutable_sequence(obj)

    Wrapper = _create_wrapper_class(obj.__class__)  # ignore: type
    return Wrapper(obj)


def to_immutable_sequence(sequence):
    return ListView(list(map(wrap_readonly, sequence)))


def to_mapping_proxy_type(mapping):
    return MappingProxyType({key: wrap_readonly(value) for key, value in mapping.items()})


@lru_cache(maxsize=None)
def _create_wrapper_class(class_: Type):
    return type(
        f"RO{class_.__name__}",
        (class_,),
        {
            "__init__": rowrapper_init,
            "__getattribute__": rowrapper_getattribute,
            "__setattr__": rowrapper_setattr,
        },
    )


def rowrapper_init(self, obj):
    object.__setattr__(self, "_obj", obj)


def rowrapper_getattribute(self, attr):
    attr_reference = getattr(object.__getattribute__(self, "_obj"), attr)

    if ismethod(attr_reference):
        return object.__getattribute__(self, attr)

    return wrap_readonly(attr_reference)


def rowrapper_setattr(self, name, value):
    raise ImmutableAttributeError(
        "Objects that are wrapped by a read-only wrapper do not support assignment"
    )
