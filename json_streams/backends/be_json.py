"""Json backend using standard `json` lib."""
import json
from typing import Any, Union

# pylint: disable=unsubscriptable-object


def dumps(obj) -> bytes:
    return json.dumps(obj).encode("utf-8")


def loads(s: Union[bytes, bytearray, str]) -> Any:
    return json.loads(s.decode("utf-8") if isinstance(s, (bytes, bytearray)) else s)
