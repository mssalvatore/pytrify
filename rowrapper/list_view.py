from collections import UserList
from typing import List, Optional


class ListView(UserList):
    def __init__(self, initlist: Optional[List] = None):
        self.data = initlist

        if self.data is None:
            self.data = []

    def __delitem__(self, *_args, **_kwargs):
        ListView._raise_type_error()

    def __iadd__(self, *_args, **_kwargs):
        ListView._raise_type_error()

    def __imul__(self, *_args, **_kwargs):
        ListView._raise_type_error()

    def __setitem__(self, *_args, **_kwargs):
        ListView._raise_type_error()

    def append(self, *_args, **_kwargs):
        ListView._raise_type_error()

    def clear(self, *_args, **_kwargs):
        ListView._raise_type_error()

    def extend(self, *_args, **_kwargs):
        ListView._raise_type_error()

    def insert(self, *_args, **_kwargs):
        ListView._raise_type_error()

    def pop(self, *_args, **_kwargs):
        ListView._raise_type_error()

    def remove(self, *_args, **_kwargs):
        ListView._raise_type_error()

    def reverse(self, *_args, **_kwargs):
        ListView._raise_type_error()

    def sort(self, *_args, **_kwargs):
        ListView._raise_type_error()

    @classmethod
    def _raise_type_error(cls):
        raise TypeError(f"'{cls.__name__}' object is immutable")
