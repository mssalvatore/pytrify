import itertools
import time

from paramutils import DynamicDefault, dynamic_defaults


class Counter:
    def __init__(self, value):
        self._initial_value = value
        self.counter = itertools.count(value)

    def __call__(self):
        return next(self.counter)

    def reset(self):
        self.counter = itertools.count(self._initial_value)


@dynamic_defaults({"timestamp"})
def fn(
    _positional1,
    _positional2,
    *,
    timestamp: DynamicDefault[float] = time.perf_counter_ns,
    _keyword=1.0
) -> float:

    t = timestamp
    time.sleep(0.001)
    # This checks that the value of `timestamp` is static, even though it was dynamically generated
    # when the function was called.
    assert t == timestamp

    return timestamp  # type: ignore


def test_fn_uses_provided_static_argument():
    input_timestamp = 1337.1337
    output_timestamp = fn(None, None, timestamp=input_timestamp)

    assert output_timestamp == input_timestamp


def test_fn_generates_uses_provided_callable():
    counter = Counter(10.0)

    output_timestamp = fn(None, None, timestamp=counter)

    assert output_timestamp == 10.0


def test_fn_uses_default_callable():
    output_timestamp = fn(None, None)
    assert output_timestamp > 1647045808.1758072


def test_fn_generates_new_dynamic_default():
    output_timestamp_1 = fn(None, None)
    output_timestamp_2 = fn(None, None)
    output_timestamp_3 = fn(None, None)

    assert output_timestamp_1 < output_timestamp_2 < output_timestamp_3


counter1 = Counter(1)
counter2 = Counter(100)


@dynamic_defaults({"actual1", "actual2"})
def check_values(
    expected1,
    expected2,
    *,
    actual1: DynamicDefault[int] = counter1,
    _dummy=None,
    actual2: DynamicDefault[int] = counter2
):
    assert expected1 == actual1
    assert expected2 == actual2


def test_multiple_default_fn():
    counter1.reset()
    counter2.reset()
    check_values(1, 100)
    check_values(2, 101)


def test_multiple_with_user_provided_fn():
    counter1.reset()
    counter2.reset()
    counter3 = Counter(42)

    check_values(42, 100, actual1=counter3)
    check_values(1, 43, actual2=counter3)
