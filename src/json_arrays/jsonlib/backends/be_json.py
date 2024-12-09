"""Json backend using standard `json` lib."""

import json


def dumps(obj, **kwargs) -> bytes:
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False, **kwargs).encode("utf-8")


loads = json.loads
