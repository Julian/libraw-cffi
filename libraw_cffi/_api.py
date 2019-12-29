from contextlib import closing
import mmap

from _raw import ffi, lib


class LibRawError(Exception):
    def __init__(self, errorcode):
        super(LibRawError, self).__init__(errorcode)
        self._message = ffi.string(lib.libraw_strerror(errorcode))

    def __str__(self):
        return self._message


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
    failed = lib.libraw_open_file(data, bytes(path))
    if failed:
        raise LibRawError(failed)
    return data


def _data():
    data = lib.libraw_init(0)
    ffi.gc(data, lib.libraw_recycle)
    return data
