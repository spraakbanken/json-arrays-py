import os
import sys
import typing

# pylint: disable=unsubscriptable-object

if sys.version_info >= (3, 9):
    Pathlike = typing.TypeVar(
        "Pathlike", str, bytes, os.PathLike[str], os.PathLike[bytes]
    )
else:
    Pathlike = typing.TypeVar("Pathlike", str, bytes, os.PathLike)
