from typing import Any, Union

def dumps(obj: Any) -> bytes: ...
def loads(s: Union[bytes, bytearray, str]) -> Any: ...
