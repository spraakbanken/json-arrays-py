import io
from unittest import mock

import pytest

import json_streams
from .utils import compare_iters


@pytest.mark.parametrize("file_name,file_type, expected_iter", [
    ("test", "json", "json_iter"),
    ("test", None, "json_iter"),
    ("test.json", None, "json_iter"),
    ("test", "jsonl", "jsonl_iter"),
    ("test.jsonl", None, "jsonl_iter"),
])
def test_dump_to_file_json(file_name, file_type, expected_iter):
    with mock.patch(
        "json_streams.json_iter.dump_to_file"
    ) as json_iter_mock, mock.patch(
        "json_streams.jsonl_iter.dump_to_file"
    ) as jsonl_iter_mock:
        in_iter = None
        json_streams.dump_to_file(in_iter, file_name, file_type=file_type)
        expected_call = [mock.call(in_iter, file_name, file_mode=None)]
        if expected_iter == "json_iter":
            assert json_iter_mock.mock_calls == expected_call
            jsonl_iter_mock.assert_not_called()
        else:
            assert jsonl_iter_mock.mock_calls == expected_call
            json_iter_mock.assert_not_called()


@pytest.mark.parametrize("out", [io.StringIO, io.BytesIO])
@pytest.mark.parametrize("data,facit,file_type", [
    (1, "1", "json"),
    (1, "1\n", "jsonl"),
    ([1, 2], "[\n1,\n2\n]", "json"),
    ([1, 2], "1\n2\n", "jsonl"),
])
def test_dump_int_memoryio(out, data, facit, file_type):
    out = out()
    if isinstance(out, io.BytesIO):
        facit = facit.encode('utf-8')
    json_streams.dump(data, out, file_type=file_type)
    assert out.getvalue() == facit

    out.seek(0)  # read it from the beginning
    out_iter = json_streams.load(out, file_type=file_type)
    if isinstance(data, list):
        compare_iters(out_iter, data)
    else:
        for i in json_streams.load(out, file_type=file_type):
            print("i = {i}".format(i=i))
            assert i == data
