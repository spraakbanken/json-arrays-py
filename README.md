# json-arrays

[![PyPI version](https://badge.fury.io/py/json-arrays.svg)](https://pypi.org/project/json-arrays/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/json-arrays)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/json-arrays)](https://pypi.org/project/json-arrays/)

[![Maturity badge - level 3](https://img.shields.io/badge/Maturity-Level%203%20--%20Stable-green.svg)](https://github.com/spraakbanken/getting-started/blob/main/scorecard.md)
[![Stage](https://img.shields.io/pypi/status/json-arrays)](https://pypi.org/project/json-arrays/)

[![Code Coverage](https://codecov.io/gh/spraakbanken/json-arrays-py/branch/main/graph/badge.svg)](https://codecov.io/gh/spraakbanken/json-arrays-py/)

[![CI(check)](https://github.com/spraakbanken/json-arrays-py/actions/workflows/check.yml/badge.svg)](https://github.com/spraakbanken/json-arrays-py/actions/workflows/check.yml)
[![CI(release)](https://github.com/spraakbanken/json-arrays-py/actions/workflows/release.yml/badge.svg)](https://github.com/spraakbanken/json-arrays-py/actions/workflows/release.yml)
[![CI(scheduled)](https://github.com/spraakbanken/json-arrays-py/actions/workflows/scheduled.yml/badge.svg)](https://github.com/spraakbanken/json-arrays-py/actions/workflows/scheduled.yml)
[![CI(test)](https://github.com/spraakbanken/json-arrays-py/actions/workflows/test.yml/badge.svg)](https://github.com/spraakbanken/json-arrays-py/actions/workflows/test.yml)

Read and write JSON lazy, especially json-arrays.

Handles both the JSON format:

```json
[
  {
    "a": 1
  },
  {
    "a": 2
  }
]
```

As well as JSON LINES format:

```json
{"a":1}
{"a": 2}
```

Also supports streaming from gzipped files.

Uses `orjson` if present, otherwise standard `json`.

## Usage

### Installation

```bash
# Using standard json
pip install json-arrays

# Using orjson
pip install json-arrays[orjson]

```

### Note

This library prefers files opened in binary mode.
Therefore does all `dumps`-methods return `bytes`.

All `loads` methods handles `str`, `bytes` and `bytesarray` arguments.

### Examples

Allows you to use `json.load` and `json.dump` with
both json and json-lines files as well as dumping generators.

```python
import json_arrays

# This command tries to guess format and opens the file
data = json_arrays.load_from_file("data.json") # or data.jsonl

# Write to file, again guessing format
json_arrays.dump_to_file(data, "data.jsonl")
```

```python
from json_arrays import json_iter, jsonl_iter

# Open and read the file without guessing
data = json_iter.load_from_file("data.json")

# Process file

# Write to file without guessing
jsonl_iter.dump_to_file(data, "data.jsonl")
```

```python
import json_arrays
def process(data):
    for entry in data:
        # process
        yield entry

def read_process_and_write(filename_in, filename_out):

    json_arrays.dump_to_file(
        process(
            json_arrays.load_from_file(filename_in)
        ),
        filename_out
    )
```

You can also use json_arrays as a sink, that you can send data to.

```python
import json_arrays

with open("out.json", "bw") as fp:
  # guessing format
  with json_arrays.sink(fp) as sink:
    for data in data_source():
      sink.send(data)
```

## Minimum Supported Python Version Policy

The Minimum Supported Python Version is fixed for a given minor (1.x)
version. However it can be increased when bumping minor versions, i.e. going
from 1.0 to 1.1 allows us to increase the Minimum Supported Python Version. Users unable to increase their
Python version can use an older minor version instead. Below is a list of sparv-sbx-conllu versions
and their Minimum Supported Python Version:

- v0.16: Python 3.10
- v0.15: Python 3.9

Note however that sparv-sbx-conllu also has dependencies, which might have different MSPV
policies. We try to stick to the above policy when updating dependencies, but
this is not always possible.

## Changelog

This project keeps a [changelog](./CHANGELOG.md).

## License

This repository is licensed under the [MIT](./LICENSE) license.

## Development

This project uses [pdm](https://pdm-project.org).
After cloning the repo, just run

```bash
make dev
make test
```

to setup a virtual environment,
install dev dependencies
and run the unit tests.

_Note:_ If you run the command in a activated virtual environment,
that environment is used instead.

## Deployment

Push a tag in the format `v\d+.\d+.\d+`to `main`-branch, to build & publish package to PyPi.
