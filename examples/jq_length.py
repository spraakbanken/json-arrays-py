"""Example to show how to count a length of a json/ndjson file."""

import sys

import json_arrays


def main() -> None:
    r"""Count number of elements in a array.

    Reads either the given path or from `stdin`.

    Example:
    `echo '{"a":1}\n{"b":2}' | python examples/jq_length.py`
    Should print 2
    """
    path = sys.argv[1] if len(sys.argv) > 1 else None
    length = sum(1 for _ in json_arrays.load_from_file(path, use_stdin_as_default=True))
    print(length)


if __name__ == "__main__":
    main()
