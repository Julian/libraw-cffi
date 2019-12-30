from contextlib import closing
import mmap
import os

from _raw import ffi, lib


class LibRawError(Exception):
    def __init__(self, message, code=None):
        super(LibRawError, self).__init__(message, code)
        self._message = message
        self._code = code

    def __str__(self):
        return self._message

    @classmethod
    def from_code(cls, code):
        return cls(
            message=ffi.string(lib.libraw_strerror(code)),
            code=code,
        )


def from_file(file, size=None):
    data = _data()
    mmapped = mmap.mmap(file.fileno(), 0, mmap.MAP_PRIVATE, mmap.PROT_READ)
    with closing(mmapped):
        lib.libraw_open_buffer(
            data,
            ffi.from_buffer(mmapped),
            mmapped.size(),
        )
    return data


def from_path(path):
    data = _data()
    _succeed(lib.libraw_open_file(data, bytes(path)))
    return data


def _succeed(errorcode):
    # Implement the behavior specified in
    # https://www.libraw.org/docs/API-notes.html#errors
    if errorcode < 0:
        raise LibRawError.from_code(errorcode)
    elif errorcode > 0:
        raise OSError(errorcode, os.strerror(errorcode))


def _data():
    data = lib.libraw_init(0)
    ffi.gc(data, lib.libraw_close)
    return data
