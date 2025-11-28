"""Writer for writing JSON arrays."""

import typing as t
from collections.abc import Iterable

from json_arrays import jsonlib, utility


class JsonArrayWriter:
    """Writer for writing JSON arrays."""

    def __init__(self, *, json_lines: bool = False) -> None:
        """Writer for writing JSON arrays.

        Args:
            json_lines: if set to True, write as json_lines
        """
        self.delimiter = b"\n" if json_lines else b","
        self._write_array_wrap = not json_lines
        self._array_end_char = b"\n" if json_lines else b"]"

    @classmethod
    def as_json_writer(cls) -> "JsonArrayWriter":
        """Create a writer for writing JSON."""
        return cls(json_lines=False)

    # @classmethod
    # def json

    def dumps(self, obj: t.Any, **kwargs: t.Any) -> Iterable[bytes]:
        """Create an Iterable of bytes as JSON from the given obj."""
        if isinstance(obj, str):
            yield jsonlib.dumps(obj, **kwargs)
        elif isinstance(obj, dict):
            yield from self._dump_dict(obj, **kwargs)
        else:
            try:
                it = iter(obj)
            except TypeError:
                yield jsonlib.dumps(obj, **kwargs)
            else:
                if self._write_array_wrap:
                    yield b"["
                for i, o in enumerate(it):
                    if i > 0:
                        yield self.delimiter
                    yield jsonlib.dumps(o, **kwargs)
                if self._write_array_wrap:
                    yield b"]"

    def _dump_dict(self, obj: dict[str, t.Any], **kwargs: t.Any) -> Iterable[bytes]:
        """Create an Iterable from the given dict."""
        yield b"{"
        for i, (key, value) in enumerate(obj.items()):
            if i > 0:
                yield b","
            yield b'"%s":' % utility.to_bytes(key)
            writer = self.as_json_writer()
            yield from writer.dumps(value, **kwargs)
        yield b"}"
