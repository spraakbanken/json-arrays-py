import tempfile
from unittest import mock

import pytest

from json_arrays import json_iter, jsonl_iter
from json_arrays.jsonlib.backends import be_json


def consume_iter(it) -> None:
    for _val in it:
        pass
    # assert sum(1 for _v in it) == expected_length


ARRAY_SMALL_JSON: str = "assets/supp-data/data/array_small.json"
ARRAY_MEDIUM_JSON: str = "assets/supp-data/data/array_medium.json"
ARRAY_LARGE_JSON: str = "assets/supp-data/data/skbl.json"
ARRAY_SMALL_NDJSON: str = "assets/supp-data/data/array_small.ndjson"
ARRAY_MEDIUM_NDJSON: str = "assets/supp-data/data/array_medium.ndjson"
ARRAY_LARGE_NDJSON: str = "assets/supp-data/data/skbl.ndjson"


@pytest.mark.benchmark(group="roundtrip-small")
def test_roundtrip_json_iter_with_lib_json_small(benchmark) -> None:
    with mock.patch("json_arrays.jsonlib") as jsonlib_patched:
        jsonlib_patched.dumps = be_json.dumps
        with tempfile.TemporaryFile() as fp:
            benchmark(lambda: json_iter.dump(json_iter.load_from_file(ARRAY_SMALL_JSON), fp))


@pytest.mark.benchmark(group="roundtrip-medium")
def test_roundtrip_json_iter_with_lib_json_medium(benchmark) -> None:
    with mock.patch("json_arrays.jsonlib") as jsonlib_patched:
        jsonlib_patched.dumps = be_json.dumps
        with tempfile.TemporaryFile() as fp:
            benchmark(lambda: json_iter.dump(json_iter.load_from_file(ARRAY_MEDIUM_JSON), fp))


@pytest.mark.benchmark(group="roundtrip-large")
def test_roundtrip_json_iter_with_lib_json_large(benchmark) -> None:
    with mock.patch("json_arrays.jsonlib") as jsonlib_patched:
        jsonlib_patched.dumps = be_json.dumps
        with tempfile.TemporaryFile() as fp:
            benchmark(lambda: json_iter.dump(json_iter.load_from_file(ARRAY_LARGE_JSON), fp))


@pytest.mark.benchmark(group="roundtrip-small")
def test_roundtrip_json_iter_with_lib_orjson_small(benchmark) -> None:
    with tempfile.TemporaryFile() as fp:
        benchmark(lambda: json_iter.dump(json_iter.load_from_file(ARRAY_SMALL_JSON), fp))


@pytest.mark.benchmark(group="roundtrip-medium")
def test_roundtrip_json_iter_with_lib_orjson_medium(benchmark) -> None:
    with tempfile.TemporaryFile() as fp:
        benchmark(lambda: json_iter.dump(json_iter.load_from_file(ARRAY_MEDIUM_JSON), fp))


@pytest.mark.benchmark(group="roundtrip-large")
def test_roundtrip_json_iter_with_lib_orjson_large(benchmark) -> None:
    with tempfile.TemporaryFile() as fp:
        benchmark(lambda: json_iter.dump(json_iter.load_from_file(ARRAY_LARGE_JSON), fp))


@pytest.mark.benchmark(group="roundtrip-small")
def test_roundtrip_jsonl_iter_with_lib_json_small(benchmark) -> None:
    with mock.patch("json_arrays.jsonlib") as jsonlib_patched:
        jsonlib_patched.loads = be_json.loads
        jsonlib_patched.dumps = be_json.dumps
        with tempfile.TemporaryFile() as fp:
            benchmark(lambda: jsonl_iter.dump(jsonl_iter.load_from_file(ARRAY_SMALL_NDJSON), fp))


@pytest.mark.benchmark(group="roundtrip-medium")
def test_roundtrip_jsonl_iter_with_lib_json_medium(benchmark) -> None:
    with mock.patch("json_arrays.jsonlib") as jsonlib_patched:
        jsonlib_patched.loads = be_json.loads
        jsonlib_patched.dumps = be_json.dumps
        with tempfile.TemporaryFile() as fp:
            benchmark(
                lambda: jsonl_iter.dump(jsonl_iter.load_from_file(ARRAY_MEDIUM_NDJSON), fp)
            )


@pytest.mark.benchmark(group="roundtrip-large")
def test_roundtrip_jsonl_iter_with_lib_json_large(benchmark) -> None:
    with mock.patch("json_arrays.jsonlib") as jsonlib_patched:
        jsonlib_patched.loads = be_json.loads
        jsonlib_patched.dumps = be_json.dumps
        with tempfile.TemporaryFile() as fp:
            benchmark(lambda: jsonl_iter.dump(jsonl_iter.load_from_file(ARRAY_LARGE_NDJSON), fp))


@pytest.mark.benchmark(group="roundtrip-small")
def test_roundtrip_jsonl_iter_with_lib_orjson_small(benchmark) -> None:
    with tempfile.TemporaryFile() as fp:
        benchmark(lambda: jsonl_iter.dump(jsonl_iter.load_from_file(ARRAY_SMALL_NDJSON), fp))


@pytest.mark.benchmark(group="roundtrip-medium")
def test_roundtrip_jsonl_iter_with_lib_orjson_medium(benchmark) -> None:
    with tempfile.TemporaryFile() as fp:
        benchmark(lambda: jsonl_iter.dump(jsonl_iter.load_from_file(ARRAY_MEDIUM_NDJSON), fp))


@pytest.mark.benchmark(group="roundtrip-large")
def test_roundtrip_jsonl_iter_with_lib_orjson_large(benchmark) -> None:
    with tempfile.TemporaryFile() as fp:
        benchmark(lambda: jsonl_iter.dump(jsonl_iter.load_from_file(ARRAY_LARGE_NDJSON), fp))
