from json_streams.utils import is_jsonl


def test_jsonl():
    file_name = "test.jsonl"
    assert is_jsonl(file_name)


def test_json():
    file_name = "test.json"
    assert not is_jsonl(file_name)
