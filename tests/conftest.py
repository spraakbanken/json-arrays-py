from typing import Generator

import pytest
from syrupy.extensions.json import JSONSnapshotExtension


@pytest.fixture
def snapshot_json(snapshot):
    return snapshot.with_defaults(extension_class=JSONSnapshotExtension)


@pytest.fixture
def array_of_dicts() -> list[dict]:
    return [{"a": "a1"}, {"b": ["b1", "b2"]}, {"c": {"c1": "c11"}}]


def make_gen(src: list) -> Generator:
    yield from src


@pytest.fixture
def data_dict_w_gen() -> dict:
    return {"a": make_gen([{"b": 2, "c": "hi", "d": [1, 2]}]), "b": [1, 2]}
