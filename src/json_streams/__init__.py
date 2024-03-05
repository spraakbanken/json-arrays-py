"""Handle JSON or JSON_LINES lazily."""
import warnings

from json_arrays import (
    dump,
    dump_to_file,
    encoders,
    json_iter,
    jsonl_iter,
    jsonlib,
    load,
    load_from_file,
    sink,
    sink_from_file,
    utility,
)

__all__ = [
    "encoders",
    "json_iter",
    "jsonl_iter",
    "jsonlib",
    "utility",
    "load",
    "load_from_file",
    "dump",
    "dump_to_file",
    "sink",
    "sink_from_file",
]

warnings.warn(
    "json_streams is renamed to json_arrays, please update dependencies",
    DeprecationWarning,
    stacklevel=2,
)
