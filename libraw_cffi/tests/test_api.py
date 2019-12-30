from unittest import TestCase

from _raw import ffi, lib
from libraw_cffi.tests import Path
import libraw_cffi


RADIOHEAD = Path(__file__).parent / "_DSC2164.ARW"
RADIOHEAD_SIZE = 5216, 3464


class TestAPI(TestCase):
    def test_from_file(self):
        with RADIOHEAD.open() as file:
            data = libraw_cffi.from_file(file)
        self.assertEqual((data.sizes.width, data.sizes.height), RADIOHEAD_SIZE)

    def test_from_path(self):
        data = libraw_cffi.from_path(RADIOHEAD)
        self.assertEqual((data.sizes.width, data.sizes.height), RADIOHEAD_SIZE)

    def test_from_nonexisting_path(self):
        with self.assertRaises(libraw_cffi.LibRawError) as e:
            libraw_cffi.from_path(Path("/some/file/that/does/not/exist"))
        self.assertIn(
            ffi.string(lib.libraw_strerror(lib.LIBRAW_IO_ERROR)),
            str(e.exception),
        )
