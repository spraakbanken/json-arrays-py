from unittest import mock

import pytest

from json_arrays import json_iter, jsonl_iter
from json_arrays.jsonlib.backends import be_json


def consume_iter(it) -> None:
    for _val in it:
        pass
    # assert sum(1 for _v in it) == expected_length


ARRAY_SMALL_JSON: str = "assets/supp-data/array_small.json"
ARRAY_MEDIUM_JSON: str = "assets/supp-data/array_medium.json"
ARRAY_LARGE_JSON: str = "assets/supp-data/data/skbl.json"
ARRAY_SMALL_NDJSON: str = "assets/supp-data/array_small.ndjson"
ARRAY_MEDIUM_NDJSON: str = "assets/supp-data/array_medium.ndjson"
ARRAY_LARGE_NDJSON: str = "assets/supp-data-gen/skbl.ndjson"


@pytest.mark.benchmark(group="load-from-file-small")
def test_load_from_file_json_iter_bm_small(benchmark) -> None:
    benchmark(consume_iter, json_iter.load_from_file(ARRAY_SMALL_JSON))


@pytest.mark.benchmark(group="load-from-file-medium")
def test_load_from_file_json_iter_bm_medium(benchmark) -> None:
    benchmark(consume_iter, json_iter.load_from_file(ARRAY_MEDIUM_JSON))


@pytest.mark.benchmark(group="load-from-file-large")
def test_load_from_file_json_iter_bm_large(benchmark) -> None:
    benchmark(consume_iter, json_iter.load_from_file(ARRAY_LARGE_JSON))


@pytest.mark.benchmark(group="load-from-file-small")
def test_load_from_file_jsonl_iter_with_lib_json_small(benchmark) -> None:
    with mock.patch("json_arrays.jsonlib") as jsonlib_patched:
        jsonlib_patched.loads = be_json.loads
        benchmark(consume_iter, jsonl_iter.load_from_file(ARRAY_SMALL_NDJSON))


@pytest.mark.benchmark(group="load-from-file-medium")
def test_load_from_file_jsonl_iter_with_lib_json_medium(benchmark) -> None:
    with mock.patch("json_arrays.jsonlib") as jsonlib_patched:
        jsonlib_patched.loads = be_json.loads
        benchmark(consume_iter, jsonl_iter.load_from_file(ARRAY_MEDIUM_NDJSON))


@pytest.mark.benchmark(group="load-from-file-large")
def test_load_from_file_jsonl_iter_with_lib_json_large(benchmark) -> None:
    with mock.patch("json_arrays.jsonlib") as jsonlib_patched:
        jsonlib_patched.loads = be_json.loads
        benchmark(consume_iter, jsonl_iter.load_from_file(ARRAY_LARGE_NDJSON))


@pytest.mark.benchmark(group="load-from-file-small")
def test_load_from_file_jsonl_iter_with_lib_orjson_small(benchmark) -> None:
    benchmark(consume_iter, jsonl_iter.load_from_file(ARRAY_SMALL_NDJSON))


@pytest.mark.benchmark(group="load-from-file-medium")
def test_load_from_file_jsonl_iter_with_lib_orjson_medium(benchmark) -> None:
    benchmark(consume_iter, jsonl_iter.load_from_file(ARRAY_MEDIUM_NDJSON))


@pytest.mark.benchmark(group="load-from-file-large")
def test_load_from_file_jsonl_iter_with_lib_orjson_large(benchmark) -> None:
    benchmark(consume_iter, jsonl_iter.load_from_file(ARRAY_LARGE_NDJSON))
