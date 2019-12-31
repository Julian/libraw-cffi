"""
A reimplementation of https://www.libraw.org/docs/API-overview.html
"""
from unittest import TestCase

from _raw import lib
from libraw_cffi.tests import RADIOHEAD, RADIOHEAD_SIZE
import libraw_cffi


class TestDemonstration(TestCase):
    def test_brief_demonstration(self):
        data = libraw_cffi.from_path(RADIOHEAD)
        self.assertEqual((data.sizes.width, data.sizes.height), RADIOHEAD_SIZE)

        lib.libraw_unpack(data)
        lib.libraw_raw2image(data)
