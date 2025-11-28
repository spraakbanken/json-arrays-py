"""Different files used in this library."""

import bz2
import gzip
import pathlib
import typing as t

from json_arrays import _types, utility


def open_file(file_name: _types.Pathlike, mode: str = "rb") -> _types.File:  # type: ignore [type-var]
    """Open a file based on extension.

    Supports ordinary files, gzip-files and bzip2-files.
    """
    assert "b" in mode
    if utility.is_gzip(file_name):
        return gzip.GzipFile(file_name, mode)  # type: ignore
    if utility.is_bzip2(file_name):
        return bz2.BZ2File(file_name, mode)  # type: ignore
    return pathlib.Path(file_name).open(mode)  # type: ignore


class BinaryFile:
    """A file to write or read binary data to."""

    def __init__(
        self,
        mode: str,
        filename: _types.Pathlike | None = None,
        fileobj: _types.File | None = None,
    ) -> None:
        """Open BinaryFile."""
        if fileobj is None and filename is None:
            raise ValueError("Must give at least one of 'filename' and 'fileobj'")

        if "t" in mode:
            raise ValueError("Only binary modes supported")
        if "b" not in mode:
            mode = f"{mode}b"
        self._needs_closing = False
        if fileobj is None:
            if filename is not None:
                self._file: _types.File = open_file(filename, mode)  # type: ignore
            else:
                raise ValueError("Must give at least one of 'filename' and 'fileobj'")

        else:
            fileobj_name = utility.get_name_of_file(fileobj)
            if utility.is_gzip(fileobj_name):
                if isinstance(fileobj, gzip.GzipFile):
                    self._file = fileobj  # type: ignore
                else:
                    self._file = gzip.GzipFile(  # type: ignore
                        filename=filename, fileobj=fileobj, mode=mode
                    )
                    self._needs_closing = True
            elif utility.is_bzip2(fileobj_name) or (filename and utility.is_bzip2(filename)):
                if isinstance(fileobj, bz2.BZ2File):
                    self._file = fileobj  # type: ignore
                else:
                    fileobj_or_filename = fileobj or filename
                    self._file = bz2.BZ2File(  # type: ignore
                        filename=fileobj_or_filename, mode=mode
                    )
                    self._needs_closing = True
            else:
                self._file = fileobj  # type: ignore

    @property
    def file(self) -> t.Any:
        """Return the underlying file."""
        return self._file  # type: ignore

    @property
    def needs_closing(self) -> bool:
        """Return True if this file needs to be closed."""
        return self._needs_closing

    def read(self) -> bytes:
        """Read bytes from the underlying file."""
        return self._file.read()  # type: ignore

    def close(self) -> None:
        """Close this file, if needed."""
        if self.needs_closing:
            self._file.close()  # type: ignore


class BinaryFileRead(BinaryFile):
    """A binary file to read from."""

    def __init__(
        self,
        filename: _types.Pathlike | None = None,
        fileobj: _types.File | None = None,
    ) -> None:
        """Create a readable binary file."""
        super().__init__("rb", filename=filename, fileobj=fileobj)


class BinaryFileWrite(BinaryFile):
    """A binary file to write to."""

    def __init__(
        self,
        filename: _types.Pathlike | None = None,
        fileobj: _types.File | None = None,
        mode: str | None = None,
    ) -> None:
        """Create a writeable binary file."""
        super().__init__(mode=mode or "wb", filename=filename, fileobj=fileobj)

    def write(self, data: bytes | bytearray) -> int:
        """Write data to the underlying file."""
        return self._file.write(data)  # type: ignore
