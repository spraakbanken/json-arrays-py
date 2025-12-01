import os
import typing as t
from collections.abc import Generator, Iterable

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


class SinkP(t.Protocol):
    """A utility that wraps a co-routine, and closes it."""

    def __init__(self, sink: Generator[None, t.Any, None]) -> None: ...

    def __enter__(self) -> Generator[None, t.Any, None]: ...

    def __exit__(self, exc_type: t.Any, exc_value: t.Any, exc_traceback: t.Any) -> None: ...


class HasDump(t.Protocol):
    """Protocol for dump."""

    def dump(self, data: dict | Iterable, fileobj: FileWrite, **kwargs: t.Any) -> None: ...


class HasDumps(t.Protocol):
    """Protocol for dumps."""

    def dumps(self, data: dict | Iterable, **kwargs: t.Any) -> Iterable[bytes]: ...


class HasDumpToFile(t.Protocol):
    """Protocol for dump_to_file."""

    def dump_to_file(
        self,
        data: dict | Iterable,
        file_name: Pathlike,
        *,
        file_mode: str = "wb",
        **kwargs: t.Any,
    ) -> None: ...


class HasLoad(t.Protocol):
    """Protocol for load."""

    def load(
        self, fileobj: FileRead, *, use_float: bool = True, **kwargs: t.Any
    ) -> Iterable: ...


class HasLoads(t.Protocol):
    """Protocol for loads."""

    def loads(self, data: dict | Iterable, **kwargs: t.Any) -> Iterable: ...


class HasLoadFromFile(t.Protocol):
    """Protocol for load_from_file."""

    def load_from_file(
        self,
        file_name: Pathlike,
        *,
        file_mode: str = "rb",
        **kwargs: t.Any,
    ) -> Iterable: ...


class HasSink(t.Protocol):
    """Protocol for sink."""

    def sink(self, fileobj: FileWrite) -> SinkP: ...


class HasSinkFromFile(t.Protocol):
    """Protocol for sink_from_file."""

    def sink_from_file(
        self,
        file_name: Pathlike,
        *,
        file_mode: str = "wb",
    ) -> SinkP: ...


class IterModule(HasDump, HasDumpToFile, HasLoad, HasLoadFromFile, HasSink, HasSinkFromFile):
    """Protocol for iter module."""


class Backend(t.Protocol):
    def dumps(self, obj: t.Any, **kwargs: t.Any) -> bytes: ...
    def loads(
        self, data: str | bytes | bytearray, **kwargs: t.Any
    ) -> dict[str, t.Any] | list[t.Any] | t.Any: ...
