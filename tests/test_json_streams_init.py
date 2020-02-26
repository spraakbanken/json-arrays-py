import io

import pytest

import json_streams
from .utils import compare_iters


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
