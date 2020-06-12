import pytest

from json_streams.utils import is_jsonl, get_name_of_file


def test_jsonl():
    file_name = "test.jsonl"
    assert is_jsonl(file_name)


def test_json():
    file_name = "test.json"
    assert not is_jsonl(file_name)


@pytest.mark.parametrize("fp, expected", [(None, "")])
def test_get_name_of_file(fp, expected):
    assert get_name_of_file(fp) == expected
