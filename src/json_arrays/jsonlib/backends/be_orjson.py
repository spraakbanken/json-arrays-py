"""Json backend using `orjson` library."""

from orjson import JSONDecodeError, JSONEncodeError, dumps, loads

__all__ = ["JSONDecodeError", "JSONEncodeError", "dumps", "loads"]
