import io
from unittest import mock

import pytest

import json_streams
from .utils import compare_iters


@pytest.mark.parametrize(
    "file_name,json_format, expected_iter",
    [
        ("test", "json", "json_iter"),
        ("test", None, "json_iter"),
        ("test.json", None, "json_iter"),
        ("test", "jsonl", "jsonl_iter"),
        ("test.jsonl", None, "jsonl_iter"),
    ],
)
def test_dump_to_file_json(file_name, json_format, expected_iter):
    with mock.patch(
        "json_streams.json_iter.dump_to_file"
    ) as json_iter_mock, mock.patch(
        "json_streams.jsonl_iter.dump_to_file"
    ) as jsonl_iter_mock:
        in_iter = None
        json_streams.dump_to_file(in_iter, file_name, json_format=json_format)
        expected_call = [mock.call(in_iter, file_name, file_mode="bw")]
        if expected_iter == "json_iter":
            assert json_iter_mock.mock_calls == expected_call
            jsonl_iter_mock.assert_not_called()
        else:
            json_iter_mock.assert_not_called()
            assert jsonl_iter_mock.mock_calls == expected_call


@pytest.mark.parametrize(
    "file_name,json_format, expected_iter",
    [
        ("test", "json", "json_iter"),
        ("test", None, "json_iter"),
        ("test.json", None, "json_iter"),
        ("test", "jsonl", "jsonl_iter"),
        ("test.jsonl", None, "jsonl_iter"),
    ],
)
def test_sink_from_file_json(file_name, json_format, expected_iter):
    with mock.patch(
        "json_streams.json_iter.sink_from_file"
    ) as json_iter_mock, mock.patch(
        "json_streams.jsonl_iter.sink_from_file"
    ) as jsonl_iter_mock:
        json_streams.sink_from_file(file_name, json_format=json_format)
        expected_call = [mock.call(file_name, file_mode="bw")]
        if expected_iter == "json_iter":
            assert json_iter_mock.mock_calls == expected_call
            jsonl_iter_mock.assert_not_called()
        else:
            json_iter_mock.assert_not_called()
            assert jsonl_iter_mock.mock_calls == expected_call


@pytest.mark.parametrize(
    "file_name,json_format, expected_iter",
    [
        ("test", "json", "json_iter"),
        ("test", None, "json_iter"),
        ("test.json", None, "json_iter"),
        ("test", "jsonl", "jsonl_iter"),
        ("test.jsonl", None, "jsonl_iter"),
    ],
)
def test_load_from_file_json(file_name, json_format, expected_iter):
    with mock.patch(
        "json_streams.json_iter.load_from_file"
    ) as json_iter_mock, mock.patch(
        "json_streams.jsonl_iter.load_from_file"
    ) as jsonl_iter_mock:
        for _ in json_streams.load_from_file(file_name, json_format=json_format):
            pass
        expected_call = mock.call(file_name, file_mode="br")
        if expected_iter == "json_iter":
            assert expected_call in json_iter_mock.mock_calls
            jsonl_iter_mock.assert_not_called()
        else:
            json_iter_mock.assert_not_called()
            assert expected_call in jsonl_iter_mock.mock_calls


@pytest.mark.parametrize(
    "data,facit,json_format",
    [
        (1, b"1", "json"),
        (1, b"1\n", "jsonl"),
        ([1, 2], b"[\n1,\n2\n]", "json"),
        ([1, 2], b"1\n2\n", "jsonl"),
    ],
)
def test_dump_int_memoryio(data, facit, json_format):
    out = io.BytesIO()
    json_streams.dump(data, out, json_format=json_format)
    assert out.getvalue() == facit

    out.seek(0)  # read it from the beginning
    out_iter = json_streams.load(out, json_format=json_format)
    if isinstance(data, list):
        compare_iters(out_iter, data)
    else:
        for i in json_streams.load(out, json_format=json_format):
            print("i = {i}".format(i=i))
            assert i == data


@pytest.mark.parametrize(
    "data,facit,json_format",
    [
        (1, b"1", "json"),
        (1, b"1\n", "jsonl"),
        ([1, 2], b"[\n1,\n2\n]", "json"),
        ([1, 2], b"1\n2\n", "jsonl"),
    ],
)
def test_sink_int_memoryio(data, facit, json_format):
    out = io.BytesIO()
    with json_streams.sink(out, json_format=json_format) as sink:
        for d in data if isinstance(data, list) else [data]:
            sink.send(d)
    assert out.getvalue() == facit
