# json-streams



[![Build Status](https://travis-ci.org/spraakbanken/json-streams-py.svg?branch=master)](https://travis-ci.org/spraakbanken/python-json-tools)
[![codecov](https://codecov.io/gh/spraakbanken/json-streams-py/branch/master/graph/badge.svg)](https://codecov.io/gh/spraakbanken/python-json-tools)
[![Build Status](https://github.com/spraakbanken/json-streams-py/workflows/Build/badge.svg)](https://github.com/spraakbanken/python-json-tools/actions)
[![PyPI status](https://badge.fury.io/py/json-streams.svg)](https://pypi.org/project/json-streams/)

Tools for working with json (especially) json-arrays.

Uses `ujson` if present, otherwise standard `json`.

## Usage

### Installation
```
pip install json-streams
```
### json-iter (`lib: sb_json_tools.jt_iter`)

Allows you to use `json.load` and `json.dump` with
both json and json-lines files as well as dumping generators.

```
from sb_json_tools import jt_iter

# This command tries to guess format and opens the file
data = jt_iter.load_from_file("data.json") # or data.jsonl

# Write to file, again guessing format
jt_iter.dump_to_file(data, "data.jsonl")
```

```
from sb_json_tools import json_iter, jsonl_iter

# Open and read the file
data = json_iter.load_from_file("data.json")

# Process file

# Write to file
jsonl_iter.dump_to_file(data, "data.jsonl")
```

# Development

After cloning the repo, just run
```
$ make test
```
to setup a virtual environment,
install dev dependencies
and run the unit tests.

*Note:* If you run the command in a activated virtual environment,
that environment is used instead.

