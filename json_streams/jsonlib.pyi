from typing import Any

PREFERRED_READ_MODE: str
PREFERRED_WRITE_MODE: str

def load_from_file(file_name: str) -> Any: ...
def dump_to_file(obj: Any, file_name: str) -> Any: ...
