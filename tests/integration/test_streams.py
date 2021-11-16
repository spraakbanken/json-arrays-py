import pytest
import json_streams


@pytest.mark.parametrize('dump_kwargs', [{}, {'default': json_streams.encoders.encode_decimal}])
@pytest.mark.parametrize('outfile', ['tests/data/gen/array.json', 'tests/data/gen/array.jsonl'])
@pytest.mark.parametrize('infile', ['tests/data/array.json', 'tests/data/array.jsonl'])
def test_streaming(infile, outfile, dump_kwargs):
    json_streams.dump_to_file(
        json_streams.load_from_file(infile),
        outfile,
        **dump_kwargs
    )
