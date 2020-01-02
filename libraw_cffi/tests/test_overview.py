"""
A reimplementation of https://www.libraw.org/docs/API-overview.html
"""
from unittest import TestCase

from libraw_cffi import Raw
from libraw_cffi.tests import RADIOHEAD, RADIOHEAD_SIZE


class TestDemonstration(TestCase):
    def test_brief_demonstration(self):
        raw = Raw.from_path(RADIOHEAD)
        self.assertEqual(
            (raw.data.sizes.width, raw.data.sizes.height),
            RADIOHEAD_SIZE,
        )

        raw.unpack()
        raw.raw2image()
