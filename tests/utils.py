import itertools
import typing as t


def assert_equal_not_none(i1: t.Any | None, i2: t.Any | None) -> None:
    assert i1 is not None
    assert i2 is not None
    assert i1 == i2


def compare_iters(it1: t.Iterable, it2: t.Iterable) -> None:
    for i1, i2 in itertools.zip_longest(it1, it2):
        assert_equal_not_none(i1, i2)
