import os
import typing as t

Pathlike = t.TypeVar("Pathlike", str, bytes, os.PathLike[str], os.PathLike[bytes])

# File = t.TypeVar("File", t.BinaryIO, gzip.GzipFile, bz2.BZ2File)


class FileRead(t.Protocol):
    """Protocol for readable file."""

    def read(self) -> bytes: ...
    def __enter__(self) -> t.Any: ...
    def __exit__(self, exc_type: t.Any, exc_value: t.Any, exc_traceback: t.Any) -> None: ...


class FileWrite(t.Protocol):
    """Protocol for writable file."""

    def write(self, data: bytes | bytearray) -> int: ...
    def __enter__(self) -> t.Any: ...
    def __exit__(self, exc_type: t.Any, exc_value: t.Any, exc_traceback: t.Any) -> None: ...
    def close(self) -> None: ...


File = FileRead | FileWrite
