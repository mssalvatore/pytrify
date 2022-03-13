import inspect
from copy import copy
from functools import wraps
from typing import Callable, Iterable, TypeVar, Union

T = TypeVar("T")
DynamicDefault = Union[Callable[[], T], T]


def dynamic_defaults(dynamic_kwargs: Iterable[str]):
    def decorator(fn: Callable):
        @wraps(fn)
        def _inner(*args, **kwargs):
            new_kwargs = copy(kwargs)
            kwonlydefaults = inspect.getfullargspec(fn).kwonlydefaults

            for kw in dynamic_kwargs:
                if kw in kwargs and not callable(kwargs[kw]):
                    continue

                default_argument_function = kwargs.get(kw, kwonlydefaults[kw])
                new_kwargs[kw] = default_argument_function()

            return fn(*args, **new_kwargs)

        return _inner

    return decorator
