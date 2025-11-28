from decimal import Decimal

from syrupy.assertion import SnapshotAssertion

from json_arrays import encoders, files, jsonlib


def test_encode_decimal(snapshot: SnapshotAssertion) -> None:
    result = jsonlib.dumps([10.20, "10.20", Decimal("10.20")], default=encoders.encode_decimal)

    assert result == snapshot


def test_load_from_file(snapshot_json: SnapshotAssertion) -> None:
    data = jsonlib.load_from_file("tests/data/array.json")

    assert data == snapshot_json


def test_dump_to_file(array_of_dicts: list[dict], snapshot: SnapshotAssertion) -> None:
    file_name = "tests/data/gen/jsonlib_array.json"
    jsonlib.dump_to_file(array_of_dicts, file_name)

    with files.BinaryFileRead(file_name).file as fp:
        bytes_written = fp.read()
    assert bytes_written == snapshot
