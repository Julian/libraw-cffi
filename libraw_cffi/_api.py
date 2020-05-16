from contextlib import closing
from functools import wraps
import mmap
import os
import sys

import attr

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
        message = ffi.string(lib.libraw_strerror(code))
        return cls(message=message.decode(), code=code)


def version():
    return ffi.string(lib.libraw_version())


def version_info():
    number = lib.libraw_versionNumber()
    patch = number & 0xFF
    number >>= 8
    minor = number & 0xFF
    number >>= 8
    major = number & 0xFF
    return major, minor, patch


def _data():
    data = lib.libraw_init(0)
    if data == ffi.NULL:
        raise LibRawError(message="Null pointer returned by libraw_init")
    return ffi.gc(data, lib.libraw_close)


@attr.s
class Raw(object):

    data = attr.ib(factory=_data)

    @classmethod
    def from_file(cls, file):
        raw = cls()
        mmapped = mmap.mmap(file.fileno(), 0, mmap.MAP_PRIVATE, mmap.PROT_READ)
        with closing(mmapped):
            raw.open_buffer(ffi.from_buffer(mmapped), mmapped.size())
        return raw

    @classmethod
    def from_path(cls, path):
        raw = cls()
        raw.open_file(os.fsencode(path))
        return raw

    def dcraw_make_mem_image(self):
        errcode = ffi.new("int *")
        processed_image = lib.libraw_dcraw_make_mem_image(self.data, errcode)
        if processed_image == ffi.NULL:
            raise LibRawError.from_code(errcode[0])
        return _ProcessedImage(contents=processed_image)

    def dcraw_make_mem_thumb(self):
        errcode = ffi.new("int *")
        processed_image = lib.libraw_dcraw_make_mem_thumb(self.data, errcode)
        if processed_image == ffi.NULL:
            raise LibRawError.from_code(errcode[0])
        return _ProcessedImage(contents=processed_image)


@attr.s
class _ProcessedImage(object):

    contents = attr.ib()

    @property
    def size(self):
        return self.contents.width, self.contents.height

    def buffer(self):
        return ffi.buffer(self.contents.data, self.contents.data_size)


def _wrap(fn):
    """
    Wrap a LibRaw function to pass the data struct and check for errors.

    For functions not taking the data struct, returns the function as-is.
    """
    signature = ffi.typeof(fn)
    if signature.args and signature.args[0].cname == "libraw_data_t *":
        if signature.result.cname == "int":
            # Implement the behavior specified in
            # https://www.libraw.org/docs/API-notes.html#errors
            def wrapper(self, *args, **kwargs):
                errorcode = fn(self.data, *args, **kwargs)
                if errorcode < 0:
                    raise LibRawError.from_code(errorcode)
                elif errorcode > 0:
                    raise OSError(errorcode, os.strerror(errorcode))
        else:
            def wrapper(self, *args, **kwargs):
                return fn(self.data, *args, **kwargs)
        return wraps(fn)(wrapper)
    else:
        return fn


prefix = "libraw_"
prefix_length = len(prefix)
for name in dir(lib):
    fn = getattr(lib, name)
    if name.startswith(prefix):
        name = name[prefix_length:]
        if hasattr(Raw, name):
            continue
        setattr(Raw, name, _wrap(fn))
