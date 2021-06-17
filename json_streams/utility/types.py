import os
import typing

Pathlike = typing.TypeVar("Pathlike", str, bytes, os.PathLike[str], os.PathLike[bytes])
