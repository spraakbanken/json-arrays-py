import gzip
import os
import typing

# pylint: disable=unsubscriptable-object

Pathlike = typing.TypeVar(
    "Pathlike", str, bytes, os.PathLike[str], os.PathLike[bytes]
)

File = typing.TypeVar("File", typing.BinaryIO, gzip.GzipFile)
