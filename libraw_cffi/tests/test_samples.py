"""
A reimplementation of the examples in the samples directory.
"""
from unittest import TestCase

try:
    from pathlib2 import Path
except ImportError:
    from pathlib import Path

from _raw import ffi, lib


class TestSamples(TestCase):
    def test_raw_identify(self):
        data = lib.libraw_init(0)
        self.addCleanup(lib.libraw_recycle, data)

        lib.libraw_open_file(
            data,
            bytes(Path(__file__).parent / "_DSC2164.ARW"),
        )
        self.assertEqual(
            (
                ffi.string(data.idata.make),
                ffi.string(data.idata.model),
                data.sizes.width,
                data.sizes.height,
            ),
            (b"Sony", b"ILCE-7RM3", 5216, 3464),
        )

        lib.libraw_adjust_sizes_info_only(data)

        self.assertEqual(
            (
                data.other.timestamp,
                data.lens.makernotes.CamID,
                ffi.string(data.shootinginfo.BodySerial),
                ffi.string(data.shootinginfo.InternalBodySerial),
                ffi.string(data.other.artist),
                data.idata.dng_version,
            ),
            (1531264727, 362, b"", b"30ff0000e608", b"", 0),
        )

        self.assertEqual(
            (
                data.lens.MinFocal,
                data.lens.MaxFocal,
                data.lens.MaxAp4MinFocal,
                data.lens.MaxAp4MaxFocal,
                data.lens.EXIF_MaxAp,
                data.lens.FocalLengthIn35mmFormat,
                ffi.string(data.lens.LensMake),
                ffi.string(data.lens.Lens),
            ),
            (
                55.0,
                210.0,
                4.5,
                6.300000190734863,
                5.595918655395508,
                193,
                b"",
                b"E 55-210mm F4.5-6.3 OSS",
            ),
        )

        self.assertEqual(
            (
                data.shootinginfo.DriveMode,
                data.shootinginfo.FocusMode,
                data.shootinginfo.MeteringMode,
                data.shootinginfo.AFPoint,
                data.shootinginfo.ExposureMode,
                data.shootinginfo.ImageStabilization,
            ),
            (-1, 3, -1, -1, -1, -1),
        )

        self.assertEqual(
            (
                ffi.string(data.lens.makernotes.body),
                data.lens.makernotes.CameraFormat,
                data.lens.makernotes.CameraMount,
                data.lens.makernotes.LensID,
                ffi.string(data.lens.makernotes.Lens),
                data.lens.makernotes.LensFormat,
                data.lens.makernotes.LensMount,
                data.lens.makernotes.FocalType,
            ),
            (b"", 2, 2, 32786, b"", 1, 2, 0),
        )

        self.assertEqual(
            (
                ffi.string(data.lens.makernotes.LensFeatures_pre),
                ffi.string(data.lens.makernotes.LensFeatures_suf),
                data.lens.makernotes.MinFocal,
                data.lens.makernotes.MaxFocal,
                data.lens.makernotes.MaxAp4MinFocal,
                data.lens.makernotes.MaxAp4MaxFocal,
                data.lens.makernotes.MinAp4MinFocal,
                data.lens.makernotes.MinAp4MaxFocal,
                data.lens.makernotes.MaxAp,
                data.lens.makernotes.MinAp,
                data.lens.makernotes.CurFocal,
                data.lens.makernotes.CurAp,
                data.lens.makernotes.MaxAp4CurFocal,
                data.lens.makernotes.MinAp4CurFocal,
            ),
            (
                b"",
                b"",
                55.0,
                210.0,
                4.5,
                6.300000190734863,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
            ),
        )

        self.assertEqual(
            (
                data.sizes.pixel_aspect,
                data.thumbnail.twidth,
                data.thumbnail.theight,
                data.sizes.raw_width,
                data.sizes.raw_height,
            ),
            (1.0, 1616, 1080, 5216, 3464),
        )

        self.assertEqual(
            (data.color.profile, ffi.string(data.color.model2)),
            (ffi.NULL, b""),
        )
