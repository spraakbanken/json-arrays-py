from syrupy.assertion import SnapshotAssertion

from json_arrays import json_iter


def test_dumps_dict(data_dict_w_gen: dict, snapshot: SnapshotAssertion) -> None:
    bytes_written = list(json_iter.dumps(data_dict_w_gen))

    assert bytes_written == snapshot
