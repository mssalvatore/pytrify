import time

from paramutils import DynamicDefault, dynamic_defaults


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
    def counter() -> float:
        counter.c += 1

        return counter.c

    counter.c = 10.0

    output_timestamp = fn(None, None, timestamp=counter)

    assert output_timestamp == 11


def test_fn_uses_default_callable():
    output_timestamp = fn(None, None)
    assert output_timestamp > 1647045808.1758072


def test_fn_generates_new_dynamic_default():
    output_timestamp_1 = fn(None, None)
    output_timestamp_2 = fn(None, None)
    output_timestamp_3 = fn(None, None)

    assert output_timestamp_1 < output_timestamp_2 < output_timestamp_3


# TODO: Test a function with multiple dynamic defaults
