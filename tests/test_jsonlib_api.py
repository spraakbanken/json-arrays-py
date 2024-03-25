from json_arrays import files, jsonlib


def test_load_from_file(snapshot_json) -> None:
    data = jsonlib.load_from_file("tests/data/array.json")

    assert data == snapshot_json


def test_dump_to_file(array_of_dicts: list[dict], snapshot) -> None:
    file_name = "tests/data/gen/jsonlib_array.json"
    jsonlib.dump_to_file(array_of_dicts, file_name)

    with files.BinaryFileRead(file_name).file as fp:
        bytes_written = fp.read()
    assert bytes_written == snapshot
