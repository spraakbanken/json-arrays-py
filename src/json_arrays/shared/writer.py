import typing

from json_arrays import jsonlib, utility


class JsonArrayWriter:
    def __init__(self) -> None:
        pass

    # @classmethod
    # def json

    def dumps(self, obj, **kwargs) -> typing.Iterable[bytes]:
        if isinstance(obj, str):
            yield jsonlib.dumps(obj, **kwargs)
        elif isinstance(obj, dict):
            yield b"{"
            for i, (key, value) in enumerate(obj.items()):
                if i > 0:
                    yield b","
                yield b'"%s":' % utility.to_bytes(key)
                yield from self.dumps(value, **kwargs)
            yield b"}"
        else:
            try:
                it = iter(obj)
            except TypeError:
                yield jsonlib.dumps(obj, **kwargs)
            else:
                yield b"["
                for i, o in enumerate(it):
                    if i > 0:
                        yield b","
                    yield jsonlib.dumps(o, **kwargs)

                yield b"]"
