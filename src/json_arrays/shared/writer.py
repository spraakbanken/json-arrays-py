import typing

from json_arrays import jsonlib, utility


class JsonArrayWriter:
    def __init__(self, *, json_lines: bool = False) -> None:
        self.delimiter = b"\n" if json_lines else b","
        self._write_array_wrap = not json_lines
        self._array_end_char = b"\n" if json_lines else b"]"

    def as_json_writer(self) -> "JsonArrayWriter":
        return JsonArrayWriter(json_lines=False)

    # @classmethod
    # def json

    def dumps(self, obj, **kwargs) -> typing.Iterable[bytes]:
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

    def _dump_dict(self, obj, **kwargs) -> typing.Iterable[bytes]:
        yield b"{"
        for i, (key, value) in enumerate(obj.items()):
            if i > 0:
                yield b","
            yield b'"%s":' % utility.to_bytes(key)
            writer = self.as_json_writer()
            yield from writer.dumps(value, **kwargs)
        yield b"}"
