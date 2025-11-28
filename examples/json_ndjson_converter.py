"""Show how to convert from/to json to/from ndjson."""

import sys

import json_arrays


def main() -> None:
    r"""Convert file from/to json from/to ndjson.

    Reads either from the first given path, give `-` to read from `stdin`.
    Writes either to the second given path or to `stdout`.

    Examples:
    `python examples/json_ndjson_converter.py input.json output.ndjson`

    `echo '{"a":1}\n{"b":2}' | python examples/json_ndjson_converter.py - > output.json`
    Should print 2
    """
    if len(sys.argv) <= 1:
        print("Usage: python examples/json_ndjson_converter.py INPUT [OUTPUT]")
        print()
        print("    INPUT is a path of input")
        print(
            "    OUTPUT is an optional path, otherwise the result is written to stdout (in JsonLines format)"  # noqa: E501
        )
        sys.exit(1)

    path_in = None if sys.argv[1] == "-" else sys.argv[1]
    path_out = sys.argv[2] if len(sys.argv) > 2 else None  # noqa: PLR2004
    json_arrays.dump_to_file(
        json_arrays.load_from_file(path_in, use_stdin_as_default=True),
        path_out,
        use_stdout_as_default=True,
    )


if __name__ == "__main__":
    main()
