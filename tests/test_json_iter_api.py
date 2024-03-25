from json_arrays import json_iter


def test_dumps_dict(data_dict_w_gen: dict, snapshot) -> None:
    bytes_written = list(json_iter.dumps(data_dict_w_gen))

    assert bytes_written == snapshot


def test_dumps_int(snapshot) -> None:
    bytes_written = list(json_iter.dumps(1234))

    assert bytes_written == snapshot


def test_dumps_str(snapshot) -> None:
    bytes_written = list(json_iter.dumps("just a\n string"))

    assert bytes_written == snapshot
