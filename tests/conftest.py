import pytest
from syrupy.extensions.json import JSONSnapshotExtension


@pytest.fixture
def snapshot_json(snapshot):
    return snapshot.with_defaults(extension_class=JSONSnapshotExtension)


@pytest.fixture
def array_of_dicts() -> list[dict]:
    return [{"a": "a1"}, {"b": ["b1", "b2"]}]
