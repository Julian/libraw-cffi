from unittest import TestCase

from libraw_cffi.tests import Path
import libraw_cffi


class TestAPI(TestCase):
    def test_load(self):
        with libraw_cffi.load(Path(__file__).parent / "_DSC2164.ARW") as data:
            self.assertEqual(
                (data.sizes.width, data.sizes.height),
                (5216, 3464),
            )

    def test_load_nonexistent_file(self):
        with self.assertRaises(libraw_cffi.LibRawError):
            with libraw_cffi.load(Path("/some/file/that/does/not/exist")):
                pass
