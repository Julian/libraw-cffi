from contextlib import contextmanager

from _raw import ffi, lib


class LibRawError(Exception):
    def __init__(self, errorcode):
        super(LibRawError, self).__init__(errorcode)
        self._message = ffi.string(lib.libraw_strerror(errorcode))

    def __str__(self):
        return self._message


@contextmanager
def load(path):
    data = lib.libraw_init(0)
    failed = lib.libraw_open_file(data, bytes(path))
    if failed:
        raise LibRawError(failed)
    yield data
    lib.libraw_recycle(data)
