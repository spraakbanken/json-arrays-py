"""Json backend using standard `json` lib."""

import json
import typing as t


def dumps(obj: t.Any, **kwargs: t.Any) -> bytes:
    """Dump the object to string and then converts the string to bytes."""
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False, **kwargs).encode("utf-8")


loads = json.loads
