import bz2

from json_arrays.files import BinaryFileRead


def test_open_bzip2_file_from_filename() -> None:
    filename = "tests/data/array.json.bz2"

    fp = BinaryFileRead(filename)
    assert isinstance(fp.file, bz2.BZ2File)


def test_open_bzip2_file_from_bz2file() -> None:
    filename = "tests/data/array.json.bz2"

    with bz2.BZ2File(filename) as fileobj:
        fp = BinaryFileRead(filename, fileobj=fileobj)
        assert isinstance(fp.file, bz2.BZ2File)
