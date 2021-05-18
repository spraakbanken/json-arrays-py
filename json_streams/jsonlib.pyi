from typing import Any, Union

PREFERRED_READ_MODE: str
PREFERRED_WRITE_MODE: str


def dumps(obj: Any) -> bytes:
    ...


def loads(s: Union[bytes, bytearray, str]) -> Any:
    ...


def load_from_file(file_name: str) -> Any:
    ...


def dump_to_file(obj: Any, file_name: str) -> Any:
    ...
