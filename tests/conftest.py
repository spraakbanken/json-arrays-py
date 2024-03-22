import pytest
from syrupy.extensions.json import JSONSnapshotExtension


@pytest.fixture
def snapshot_json(snapshot):
    return snapshot.with_defaults(extension_class=JSONSnapshotExtension)
