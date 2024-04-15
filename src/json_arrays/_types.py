import bz2
import gzip
import os
import typing

Pathlike = typing.TypeVar("Pathlike", str, bytes, os.PathLike[str], os.PathLike[bytes])

File = typing.TypeVar("File", typing.BinaryIO, gzip.GzipFile, bz2.BZ2File)
