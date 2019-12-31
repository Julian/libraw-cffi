"""
A reimplementation of the examples in the samples directory.
"""
from datetime import datetime
from unittest import TestCase

from _raw import ffi, lib
from libraw_cffi.tests import RADIOHEAD, RADIOHEAD_SIZE
import libraw_cffi


class TestSamples(TestCase):
    def test_raw_identify(self):
        data = libraw_cffi.from_path(RADIOHEAD)

        self.assertEqual(
            (
                ffi.string(data.idata.make),
                ffi.string(data.idata.model),
                data.sizes.width,
                data.sizes.height,
            ),
            (b"Sony", b"ILCE-7RM3") + RADIOHEAD_SIZE,
        )

        lib.libraw_adjust_sizes_info_only(data)

        self.assertEqual(
            (
                # Whee.. this looks like a naive datetime stored in the ARW
                datetime.fromtimestamp(data.other.timestamp),
                data.lens.makernotes.CamID,
                ffi.string(data.shootinginfo.BodySerial),
                ffi.string(data.shootinginfo.InternalBodySerial),
                ffi.string(data.other.artist),
                data.idata.dng_version,
            ),
            (
                datetime(
                    month=7, day=11, year=2018, hour=1, minute=18, second=47,
                ),
                0x16a,
                b"",
                b"30ff0000e608",
                b"",
                0,
            ),
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
                data.sizes.iwidth,
                data.sizes.iheight,
            ),
            (1.0, 1616, 1080, 5216, 3464, 5216, 3464),
        )

        self.assertEqual(
            (
                data.sizes.raw_crop.cwidth,
                data.sizes.raw_crop.cheight,
                data.sizes.raw_crop.cleft,
                data.sizes.raw_crop.ctop,
            ),
            (5168, 3448, 8, 8),
        )
        self.assertEqual(
            (
                data.idata.colors,
                ffi.string(data.idata.cdesc),
                list(data.color.linear_max),
            ), (
                3,
                b"RGBG",
                [15360] * 4,
            ),
        )

        self.assertEqual(
            (
                list(data.color.cam_mul),
                [list(coeffs) for coeffs in data.color.WB_Coeffs if coeffs[0]],
                [
                    list(data.color.rgb_cam[i])
                    for i in range(data.idata.colors)
                ],
                [
                    list(data.color.cam_xyz[i])
                    for i in range(data.idata.colors)
                ],
                [
                    list(data.color.ccm[i])
                    for i in range(data.idata.colors)
                ],
                [data.color.pre_mul[i] for i in range(data.idata.colors)],
            ), (
                [2528.0, 1024.0, 1564.0, 1024.0], [
                    [2452, 1024, 1640, 1024],
                    [1492, 1024, 3016, 1024],
                    [2696, 1024, 1460, 1024],
                    [2660, 1024, 1500, 1024],
                    [2944, 1024, 1348, 1024],
                    [2656, 1024, 1588, 1024],
                    [2364, 1024, 1724, 1024],
                    [2220, 1024, 2344, 1024],
                    [1760, 1024, 2892, 1024],
                    [1672, 1024, 2600, 1024],
                    [2528, 1024, 1564, 1024],
                ], [
                    [
                        1.7365375757217407,
                        -0.5611968040466309,
                        -0.17534084618091583,
                        0.0,
                    ], [
                        -0.15308751165866852,
                        1.5583630800247192,
                        -0.4052755832672119,
                        0.0,
                    ], [
                        0.01987767033278942,
                        -0.4041007161140442,
                        1.3842231035232544,
                        0.0,
                    ],
                ], [
                    [
                        0.6639999747276306,
                        -0.18469999730587006,
                        -0.0502999983727932,
                    ], [
                        -0.5238000154495239,
                        1.3009999990463257,
                        0.24740000069141388,
                    ], [
                        -0.09929999709129333,
                        0.1673000007867813,
                        0.6527000069618225,
                    ],
                ], [
                    [
                        1.1270772218704224,
                        -0.2003910094499588,
                        0.07331378012895584,
                        0.0,
                    ], [
                        0.013671875,
                        1.10546875,
                        -0.119140625,
                        0.0,
                    ], [
                        0.03125,
                        -0.0556640625,
                        1.0244140625,
                        0.0,
                    ],
                ],
                [2.553339719772339, 0.932383120059967, 1.2761651277542114],
            ),
        )
        self.assertEqual(
            (data.color.profile, ffi.string(data.color.model2)),
            (ffi.NULL, b""),
        )
