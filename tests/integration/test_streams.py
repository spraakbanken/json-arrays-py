import json_streams
import pytest


@pytest.mark.parametrize(
    "dump_kwargs", [{}, {"default": json_streams.encoders.encode_decimal}]
)
@pytest.mark.parametrize(
    "outfile", ["tests/data/gen/array.json", "tests/data/gen/array.jsonl"]
)
@pytest.mark.parametrize("infile", ["tests/data/array.json", "tests/data/array.jsonl"])
def test_streaming(infile, outfile, dump_kwargs):
    json_streams.dump_to_file(
        json_streams.load_from_file(infile), outfile, **dump_kwargs
    )


class TestLoadFromFile:
    def test_behaves_same_for_json_and_jsonl(self) -> None:
        loaded_from_json = list(json_streams.load_from_file("tests/data/array.json"))
        loaded_from_json_lines = list(
            json_streams.load_from_file("tests/data/array.jsonl")
        )

        assert loaded_from_json == loaded_from_json_lines
