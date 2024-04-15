import bz2
import gzip
import io
import json
import tempfile
from pathlib import Path
from typing import Optional
from unittest.mock import patch

import json_arrays
import pytest
from json_arrays import files
from json_arrays.utility import JsonFormat


@pytest.mark.parametrize(
    "file_name",
    [
        "tests/data/array.json",
        "tests/data/array.jsonl",
        "tests/data/array.ndjson",
        "tests/data/array.json.gz",
        "tests/data/array.jsonl.gz",
        "tests/data/array.ndjson.gz",
        "tests/data/array.json.bz2",
        "tests/data/array.jsonl.bz2",
        "tests/data/array.ndjson.bz2",
    ],
)
def test_load_from_file(file_name: str, snapshot_json):
    assert list(json_arrays.load_from_file(file_name)) == snapshot_json


@pytest.mark.parametrize(
    "file_name",
    [
        "tests/data/array.json",
        "tests/data/array.jsonl",
        "tests/data/array.ndjson",
    ],
)
def test_load(file_name: str, snapshot_json) -> None:
    with open(file_name, mode="rb") as fp:
        data_loaded = list(json_arrays.load(fp))

    assert data_loaded == snapshot_json


@pytest.mark.parametrize(
    "file_name, json_format",
    [
        ("tests/data/array.json", JsonFormat.JSON),
        ("tests/data/array.jsonl", None),
        ("tests/data/array.jsonl", JsonFormat.JSON_LINES),
    ],
)
def test_load_from_file_stdin(
    file_name: str, json_format: Optional[json_arrays.JsonFormat], snapshot_json
) -> None:
    buffer = io.BytesIO(Path(file_name).read_bytes())
    stdin_patcher = patch("sys.stdin", buffer=buffer)
    with stdin_patcher.start():
        data_loaded = list(
            json_arrays.load_from_file(
                file_name=None, json_format=json_format, use_stdin_as_default=True
            )
        )

    assert data_loaded == snapshot_json


@pytest.mark.parametrize(
    "json_format", [json_arrays.JsonFormat.JSON, json_arrays.JsonFormat.JSON_LINES]
)
def test_dump(json_format: json_arrays.JsonFormat, snapshot, array_of_dicts: list[dict]) -> None:
    with tempfile.TemporaryFile() as fp:
        json_arrays.dump(array_of_dicts, fp, json_format=json_format)
        fp.seek(0)
        data_written = fp.read()

    assert data_written == snapshot


@pytest.mark.parametrize(
    "json_format", [json_arrays.JsonFormat.JSON, json_arrays.JsonFormat.JSON_LINES]
)
def test_dump_dict(json_format: json_arrays.JsonFormat, snapshot, data_dict: dict) -> None:
    with tempfile.TemporaryFile() as fp:
        json_arrays.dump(data_dict, fp, json_format=json_format)
        fp.seek(0)
        data_written = fp.read()

    assert data_written == snapshot


@pytest.mark.parametrize(
    "json_format", [json_arrays.JsonFormat.JSON, json_arrays.JsonFormat.JSON_LINES]
)
def test_dump_int(json_format: json_arrays.JsonFormat, snapshot) -> None:
    with tempfile.TemporaryFile() as fp:
        json_arrays.dump(1234, fp, json_format=json_format)
        fp.seek(0)
        data_written = fp.read()

    assert data_written == snapshot


@pytest.mark.parametrize(
    "json_format", [json_arrays.JsonFormat.JSON, json_arrays.JsonFormat.JSON_LINES]
)
def test_dump_str(json_format: json_arrays.JsonFormat, snapshot) -> None:
    with tempfile.TemporaryFile() as fp:
        json_arrays.dump("just an ordinary\n string", fp, json_format=json_format)
        fp.seek(0)
        data_written = fp.read()

    assert data_written == snapshot


@pytest.mark.parametrize(
    "file_name",
    [
        "tests/data/gen/api_dump_array.json",
        "tests/data/gen/api_dump_array.jsonl",
        "tests/data/gen/api_dump_array.ndjson",
        "tests/data/gen/api_dump_array.json.gz",
        "tests/data/gen/api_dump_array.jsonl.gz",
        "tests/data/gen/api_dump_array.ndjson.gz",
        "tests/data/gen/api_dump_array.json.bz2",
        "tests/data/gen/api_dump_array.jsonl.bz2",
        "tests/data/gen/api_dump_array.ndjson.bz2",
    ],
)
def test_dump_to_file(file_name: str, snapshot, array_of_dicts: list[dict]) -> None:
    json_arrays.dump_to_file(array_of_dicts, file_name)

    with files.BinaryFileRead(file_name).file as fp:
        bytes_written = fp.read()
    assert bytes_written == snapshot


@pytest.mark.parametrize(
    "json_format", [None, json_arrays.JsonFormat.JSON, json_arrays.JsonFormat.JSON_LINES]
)
def test_dump_to_file_stdout(
    json_format: Optional[json_arrays.JsonFormat], snapshot, array_of_dicts: list[dict]
) -> None:
    buffer = io.BytesIO()
    stdout_patcher = patch("sys.stdout", buffer=buffer)
    with stdout_patcher.start():
        json_arrays.dump_to_file(
            array_of_dicts, file_name=None, json_format=json_format, use_stdout_as_default=True
        )

        data_written = buffer.getvalue()

    assert data_written == snapshot


@pytest.mark.parametrize(
    "json_format", [None, json_arrays.JsonFormat.JSON, json_arrays.JsonFormat.JSON_LINES]
)
def test_dump_to_file_stderr(
    json_format: Optional[json_arrays.JsonFormat], snapshot, array_of_dicts: list[dict]
) -> None:
    buffer = io.BytesIO()
    stderr_patcher = patch("sys.stderr", buffer=buffer)
    with stderr_patcher.start():
        json_arrays.dump_to_file(
            array_of_dicts, file_name=None, json_format=json_format, use_stderr_as_default=True
        )

        data_written = buffer.getvalue()

    assert data_written == snapshot


@pytest.mark.parametrize("file_suffix", [".json", ".jsonl", ".ndjson"])
def test_sink(file_suffix: str, snapshot, array_of_dicts: list[dict]) -> None:
    with tempfile.NamedTemporaryFile(suffix=file_suffix) as fp:
        with json_arrays.sink(fp) as sink:  # type: ignore[arg-type]
            for obj in array_of_dicts:
                sink.send(obj)
        fp.seek(0)
        data_written = fp.read()

    assert data_written == snapshot


@pytest.mark.parametrize("file_suffix", [".json", ".jsonl", ".ndjson"])
def test_sink_dict(file_suffix: str, snapshot) -> None:
    with tempfile.NamedTemporaryFile(suffix=file_suffix) as fp:
        with json_arrays.sink(fp) as sink:  # type: ignore[arg-type]
            sink.send({"a": "b"})
        fp.seek(0)
        data_written = fp.read()

    assert data_written == snapshot


@pytest.mark.parametrize(
    "file_name",
    [
        "tests/data/gen/api_sink_array.json",
        "tests/data/gen/api_sink_array.jsonl",
        "tests/data/gen/api_sink_array.ndjson",
        "tests/data/gen/api_sink_array.json.gz",
        "tests/data/gen/api_sink_array.jsonl.gz",
        "tests/data/gen/api_sink_array.ndjson.gz",
        "tests/data/gen/api_sink_array.json.bz2",
        "tests/data/gen/api_sink_array.jsonl.bz2",
        "tests/data/gen/api_sink_array.ndjson.bz2",
    ],
)
def test_sink_from_file(file_name: str, snapshot, array_of_dicts: list[dict]) -> None:
    with json_arrays.sink_from_file(file_name) as sink:
        for obj in array_of_dicts:
            sink.send(obj)

    with files.BinaryFileRead(file_name).file as fp:
        bytes_written = fp.read()
    assert bytes_written == snapshot


@pytest.mark.parametrize(
    "json_format", [None, json_arrays.JsonFormat.JSON, json_arrays.JsonFormat.JSON_LINES]
)
def test_sink_from_file_stdout(
    json_format: Optional[json_arrays.JsonFormat], snapshot, array_of_dicts: list[dict]
) -> None:
    buffer = io.BytesIO()
    stdout_patcher = patch("sys.stdout", buffer=buffer)
    with stdout_patcher.start():
        with json_arrays.sink_from_file(
            file_name=None, json_format=json_format, use_stdout_as_default=True
        ) as sink:
            for obj in array_of_dicts:
                sink.send(obj)

        data_written = buffer.getvalue()

    assert data_written == snapshot


def test_load_from_file_fails_without_file_name(snapshot) -> None:
    try:
        for _ in json_arrays.load_from_file(None, use_stdin_as_default=False):
            pass
    except ValueError as exc:
        assert str(exc) == snapshot


def test_dump_to_file_fails_without_file_name(snapshot) -> None:
    try:
        json_arrays.dump_to_file(
            [], None, use_stdout_as_default=False, use_stderr_as_default=False
        )
    except ValueError as exc:
        assert str(exc) == snapshot


def test_sink_from_file_fails_without_file_name(snapshot) -> None:
    try:
        json_arrays.sink_from_file(
            None, use_stdout_as_default=False, use_stderr_as_default=False
        )
    except ValueError as exc:
        assert str(exc) == snapshot


def test_json_gzip_dump_fp(array_of_dicts: list[dict], snapshot_json):
    filename = Path("tests/data/gen/json_gzip_dump_fp.json.gz")

    with open(filename, "wb") as fp:
        json_arrays.dump(array_of_dicts, fp)

    with gzip.open(filename) as fp:  # type: ignore
        loaded_entries = json.load(fp)

    assert loaded_entries == snapshot_json


def test_json_gzip_load_fp(array_of_dicts: list[dict], snapshot_json):
    filename = Path("tests/data/gen/json_gzip_load_fp.json.gz")

    with gzip.open(filename, "wt") as fp:
        json.dump(array_of_dicts, fp)

    with open(filename, "rb") as fp:  # type: ignore
        loaded_entries = list(json_arrays.load(fp))  # type: ignore

    assert loaded_entries == snapshot_json


def test_json_bzip2_dump_fp(array_of_dicts: list[dict], snapshot_json):
    filename = Path("tests/data/gen/json_bzip2_dump_fp.json.bz2")

    with open(filename, "wb") as fp:
        json_arrays.dump(array_of_dicts, fp)

    with bz2.open(filename) as fp:  # type: ignore
        loaded_entries = json.load(fp)

    assert loaded_entries == snapshot_json


def test_json_bzip2_load_fp(array_of_dicts: list[dict], snapshot_json):
    filename = Path("tests/data/gen/json_bzip2_load_fp.json.bz2")

    with bz2.open(filename, "wt") as fp:
        json.dump(array_of_dicts, fp)

    with open(filename, "rb") as fp:  # type: ignore
        loaded_entries = list(json_arrays.load(fp))  # type: ignore

    assert loaded_entries == snapshot_json


def test_json_bzip2_load_fileobj(array_of_dicts: list[dict], snapshot_json):
    filename = Path("tests/data/gen/json_bzip2_load_fileobj.json.bz2")

    with bz2.open(filename, "wt") as fp:
        json.dump(array_of_dicts, fp)

    fp = bz2.BZ2File(filename, "rb")  # type: ignore
    loaded_entries = list(json_arrays.load(fp))  # type: ignore

    assert loaded_entries == snapshot_json
