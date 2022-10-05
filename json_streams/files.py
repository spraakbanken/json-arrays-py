import builtins
import gzip
from typing import Any, Optional

from json_streams import types, utility

# pylint: disable=redefined-builtin


def open_file(file_name: types.Pathlike, mode="rb") -> types.File:
    assert "b" in mode
    if utility.is_gzip(file_name):
        return gzip.GzipFile(file_name, mode)  # type: ignore
    else:
        return builtins.open(file_name, mode)  # type: ignore


class BinaryFile:
    def __init__(
        self,
        mode: str,
        filename: Optional[types.Pathlike] = None,
        fileobj: Optional[types.File] = None,
    ) -> None:
        if fileobj is None and filename is None:
            raise ValueError("Must give at least one of 'filename' and 'fileobj'")

        if "t" in mode:
            raise ValueError("Only binary modes supported")
        elif "b" not in mode:
            mode = f"{mode}b"

        if fileobj is None:
            self._file = open_file(filename, mode)  # type: ignore

        else:
            fileobj_name = utility.get_name_of_file(fileobj)
            if utility.is_gzip(fileobj_name):
                if isinstance(fileobj, gzip.GzipFile):
                    self._file = fileobj  # type: ignore
                else:
                    self._file = gzip.GzipFile(filename=filename, fileobj=fileobj, mode=mode)  # type: ignore
            else:
                self._file = fileobj  # type: ignore

    @property
    def file(self):
        return self._file


class BinaryFileRead(BinaryFile):
    def __init__(
        self,
        filename: Optional[types.Pathlike] = None,
        fileobj: Optional[types.File] = None,
    ) -> None:

        super().__init__("rb", filename=filename, fileobj=fileobj)


class BinaryFileWrite(BinaryFile):
    def __init__(
        self,
        filename: Optional[types.Pathlike] = None,
        fileobj: Optional[types.File] = None,
        mode: Optional[str] = None,
    ) -> None:

        super().__init__(mode=mode or "wb", filename=filename, fileobj=fileobj)

    def write(self, data: Any) -> int:
        return self._file.write(data)
