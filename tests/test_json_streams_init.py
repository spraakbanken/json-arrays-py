import io
from unittest import mock

import json_streams
import pytest

from tests.utils import compare_iters


@pytest.mark.parametrize(
    "file_name,json_format, expected_iter",
    [
        ("test", "json", "json_iter"),
        ("test", None, "json_iter"),
        ("test.json", None, "json_iter"),
        ("test", "jsonl", "jsonl_iter"),
        ("test.jsonl", None, "jsonl_iter"),
        ("test.jl", None, "jsonl_iter"),
        ("test.gz", "json", "json_iter"),
        ("test.gz", None, "json_iter"),
        ("test.json.gz", None, "json_iter"),
        ("test.gz", "jsonl", "jsonl_iter"),
        ("test.jl.gz", None, "jsonl_iter"),
        ("test.jsonl.gz", None, "jsonl_iter"),
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
        expected_call = [mock.call(in_iter, file_name, file_mode="wb")]
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
        ("test.jl", None, "jsonl_iter"),
        ("test.gz", "json", "json_iter"),
        ("test.gz", None, "json_iter"),
        ("test.json.gz", None, "json_iter"),
        ("test.gz", "jsonl", "jsonl_iter"),
        ("test.jl.gz", None, "jsonl_iter"),
        ("test.jsonl.gz", None, "jsonl_iter"),
    ],
)
def test_sink_from_file_json(file_name, json_format, expected_iter):
    with mock.patch(
        "json_streams.json_iter.sink_from_file"
    ) as json_iter_mock, mock.patch(
        "json_streams.jsonl_iter.sink_from_file"
    ) as jsonl_iter_mock:
        json_streams.sink_from_file(file_name, json_format=json_format)
        expected_call = [mock.call(file_name, file_mode="wb")]
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
        ("test.jl", None, "jsonl_iter"),
        ("test.gz", "json", "json_iter"),
        ("test.gz", None, "json_iter"),
        ("test.json.gz", None, "json_iter"),
        ("test.gz", "jsonl", "jsonl_iter"),
        ("test.jl.gz", None, "jsonl_iter"),
        ("test.jsonl.gz", None, "jsonl_iter"),
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
        expected_call = mock.call(file_name, file_mode="rb")
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
        ([1, 2], b"[1,2]", "json"),
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
        for d in (
            data if isinstance(data, list) else [data]
        ):  # sourcery skip: no-loop-in-tests
            sink.send(d)
    assert out.getvalue() == facit


def test_load_from_file_fails_without_file_name() -> None:
    try:
        next(json_streams.load_from_file(None, use_stdin_as_default=False))
    except ValueError as exc:
        assert str(exc) == "You must give a FILENAME or USE_STDIN_AS_DEFAULT=`True`"


def test_dump_to_file_fails_without_file_name() -> None:
    try:
        json_streams.dump_to_file(
            [], None, use_stdout_as_default=False, use_stderr_as_default=False
        )
    except ValueError as exc:
        assert (
            str(exc)
            == "You must give a FILENAME or USE_STDOUT_AS_DEFAULT=`True` or USE_STDERR_AS_DEFAULT=`True`"  # noqa: E501
        )


def test_sink_from_file_fails_without_file_name() -> None:
    try:
        json_streams.sink_from_file(
            None, use_stdout_as_default=False, use_stderr_as_default=False
        )
    except ValueError as exc:
        assert (
            str(exc)
            == "You must give a FILENAME or USE_STDOUT_AS_DEFAULT=`True` or USE_STDERR_AS_DEFAULT=`True`"  # noqa: E501
        )
