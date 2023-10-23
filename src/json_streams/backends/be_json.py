"""Json backend using standard `json` lib."""
import json
from typing import Any, Union


def dumps(obj, **kwargs) -> bytes:
    return json.dumps(obj, **kwargs).encode("utf-8")


def loads(s: Union[bytes, bytearray, str], **kwargs) -> Any:
    return json.loads(
        s.decode("utf-8") if isinstance(s, (bytes, bytearray)) else s, **kwargs
    )
