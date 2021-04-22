# json-streams

[![Build Status](https://travis-ci.org/spraakbanken/json-streams-py.svg?branch=master)](https://travis-ci.org/spraakbanken/json-streams-py)
[![codecov](https://codecov.io/gh/spraakbanken/json-streams-py/branch/master/graph/badge.svg)](https://codecov.io/gh/spraakbanken/json-streams-py/)
[![Build & Publish](https://github.com/spraakbanken/json-streams-py/workflows/Build%20&%20Publish/badge.svg)](https://github.com/spraakbanken/json-streams-py/actions)
[![PyPI status](https://badge.fury.io/py/json-streams.svg)](https://pypi.org/project/json-streams/)

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

Uses `orjson` or `ujson` if present, otherwise standard `json`.

## Usage

### Installation

```bash
# Using standard json
pip install json-streams

# Using orjson
pip install json-streams[orjson]

# Using ujson
pip install json-streams[ujson]
```

### Note

This library prefers files opened in binary mode.
Therefore does all `dumps`-methods return `bytes`.

All `loads` methods handles `str` argument.
If you use the `orjson` library you can also pass `bytes` or `bytesarray` to `loads`.
The goal is to have all `loads` handling `str`, `bytes` and `bytesarray`.

### Examples

Allows you to use `json.load` and `json.dump` with
both json and json-lines files as well as dumping generators.

```python
import json_streams

# This command tries to guess format and opens the file
data = json_streams.load_from_file("data.json") # or data.jsonl

# Write to file, again guessing format
json_streams.dump_to_file(data, "data.jsonl")
```

```python
from json_streams import json_iter, jsonl_iter

# Open and read the file without guessing
data = json_iter.load_from_file("data.json")

# Process file

# Write to file without guessing
jsonl_iter.dump_to_file(data, "data.jsonl")
```

```python
import json_streams
def process(data):
    for entry in data:
        # process
        yield entry

def read_process_and_write(filename_in, filename_out):

    json_streams.dump_to_file(
        process(
            json_streams.load_from_file(filename_in)
        ),
        filename_out
    )
```

You can also use json_streams as a sink, that you can send data to.

```python
import json_streams

with open("out.json", "bw") as fp:
  # guessing format
  with json_streams.sink(fp) as sink:
    for data in data_source():
      sink.send(data)
```

# Development

After cloning the repo, just run

```
$ make test
```

to setup a virtual environment,
install dev dependencies
and run the unit tests.

_Note:_ If you run the command in a activated virtual environment,
that environment is used instead.

# Deplovment

Push a tag in the format `v\d+.\d+.\d+`to master, to build & publish package to PyPi.
