from cffi import FFI


ffi = FFI()


ffi.set_source(
    "_raw",
    """
    #include "libraw/libraw.h"
    """,
    libraries=["raw"],
)

ffi.cdef(
    """
  typedef int... time_t;

  typedef char... uchar;
  typedef int... ushort;

  typedef int... INT64;

  /* -*- C++ -*-
  * File: libraw.h
  * Copyright 2008-2019 LibRaw LLC (info@libraw.org)
  * Created: Sat Mar  8, 2008
  *
  * LibRaw C++ interface
  *

  LibRaw is free software; you can redistribute it and/or modify
  it under the terms of the one of two licenses as you choose:

  1. GNU LESSER GENERAL PUBLIC LICENSE version 2.1
  (See file LICENSE.LGPL provided in LibRaw distribution archive for details).

  2. COMMON DEVELOPMENT AND DISTRIBUTION LICENSE (CDDL) Version 1.0
  (See file LICENSE.CDDL provided in LibRaw distribution archive for details).

  */

  enum LibRaw_errors
  {
    LIBRAW_IO_ERROR,
    ...
  };

  typedef struct
  {
    const char *decoder_name;
    unsigned decoder_flags;
  } libraw_decoder_info_t;

  typedef void (*memory_callback)(void *data, const char *file, const char *where);
  typedef void (*exif_parser_callback)(void *context, int tag, int type, int len, unsigned int ord, void *ifp);

  DllDef void default_memory_callback(void *data, const char *file, const char *where);

  typedef void (*data_callback)(void *data, const char *file, const int offset);

  DllDef void default_data_callback(void *data, const char *file, const int offset);

  typedef int (*progress_callback)(void *data, enum LibRaw_progress stage, int iteration, int expected);
  typedef int (*pre_identify_callback)(void *ctx);
  typedef void (*post_identify_callback)(void *ctx);
  typedef void (*process_step_callback)(void *ctx);

  typedef struct
  {
    memory_callback mem_cb;
    void *memcb_data;

    data_callback data_cb;
    void *datacb_data;

    progress_callback progress_cb;
    void *progresscb_data;

    exif_parser_callback exif_cb;
    void *exifparser_data;
    pre_identify_callback pre_identify_cb;
    post_identify_callback post_identify_cb;
    process_step_callback pre_subtractblack_cb, pre_scalecolors_cb, pre_preinterpolate_cb, pre_interpolate_cb,
                        interpolate_bayer_cb, interpolate_xtrans_cb,
                        post_interpolate_cb, pre_converttorgb_cb, post_converttorgb_cb;
  } libraw_callbacks_t;

  typedef struct
  {
    enum LibRaw_image_formats type;
    ushort height, width, colors, bits;
    unsigned int data_size;
    unsigned char data[1];
  } libraw_processed_image_t;

  typedef struct
  {
    char guard[4];
    char make[64];
    char model[64];
    char software[64];
    unsigned raw_count;
    unsigned dng_version;
    unsigned is_foveon;
    int colors;
    unsigned filters;
    char xtrans[6][6];
    char xtrans_abs[6][6];
    char cdesc[5];
    unsigned xmplen;
    char *xmpdata;
  } libraw_iparams_t;

  typedef struct
  {
    ushort cleft, ctop, cwidth, cheight;
  } libraw_raw_crop_t;

  typedef struct
  {
    ushort raw_height, raw_width, height, width, top_margin, left_margin;
    ushort iheight, iwidth;
    unsigned raw_pitch;
    double pixel_aspect;
    int flip;
    int mask[8][4];
    libraw_raw_crop_t raw_crop;
  } libraw_image_sizes_t;

  struct ph1_t
  {
    int format, key_off, tag_21a;
    int t_black, split_col, black_col, split_row, black_row;
    float tag_210;
  };

  typedef struct
  {
    unsigned parsedfields;
    ushort illuminant;
    float calibration[4][4];
    float colormatrix[4][3];
    float forwardmatrix[3][4];
  } libraw_dng_color_t;

  typedef struct
  {
    unsigned parsedfields;
    unsigned dng_cblack[4102];
    unsigned dng_black;
    unsigned dng_whitelevel[4];
    unsigned default_crop[4]; /* Origin and size */
    unsigned preview_colorspace;
    float analogbalance[4];
  } libraw_dng_levels_t;

  typedef struct
  {
    float romm_cam[9];
  } libraw_P1_color_t;

  typedef struct
  {
    int CanonColorDataVer;
    int CanonColorDataSubVer;
    int SpecularWhiteLevel;
    int NormalWhiteLevel;
    int ChannelBlackLevel[4];
    int AverageBlackLevel;
    /* multishot */
    unsigned int multishot[4];
    /* metering */
    short MeteringMode;
    short SpotMeteringMode;
    uchar FlashMeteringMode;
    short FlashExposureLock;
    short ExposureMode;
    short AESetting;
    uchar HighlightTonePriority;
    /* stabilization */
    short ImageStabilization;
    /* focus */
    short FocusMode;
    short AFPoint;
    short FocusContinuous;
    short AFPointsInFocus30D;
    uchar AFPointsInFocus1D[8];
    ushort AFPointsInFocus5D; /* bytes in reverse*/
                              /* AFInfo */
    ushort AFAreaMode;
    ushort NumAFPoints;
    ushort ValidAFPoints;
    ushort AFImageWidth;
    ushort AFImageHeight;
    short AFAreaWidths[61];     /* cycle to NumAFPoints */
    short AFAreaHeights[61];    /* --''--               */
    short AFAreaXPositions[61]; /* --''--               */
    short AFAreaYPositions[61]; /* --''--               */
    short AFPointsInFocus[4];   /* cycle to floor((NumAFPoints+15)/16) */
    short AFPointsSelected[4];  /* --''--               */
    ushort PrimaryAFPoint;
    /* flash */
    short FlashMode;
    short FlashActivity;
    short FlashBits;
    short ManualFlashOutput;
    short FlashOutput;
    short FlashGuideNumber;
    /* drive */
    short ContinuousDrive;
    /* sensor */
    short SensorWidth;
    short SensorHeight;
    short SensorLeftBorder;
    short SensorTopBorder;
    short SensorRightBorder;
    short SensorBottomBorder;
    short BlackMaskLeftBorder;
    short BlackMaskTopBorder;
    short BlackMaskRightBorder;
    short BlackMaskBottomBorder;
    int AFMicroAdjMode;
    float AFMicroAdjValue;

  } libraw_canon_makernotes_t;

  typedef struct
  {
    int BaseISO;
    double Gain;
  } libraw_hasselblad_makernotes_t;

  typedef struct
  {
    float FujiExpoMidPointShift;
    ushort FujiDynamicRange;
    ushort FujiFilmMode;
    ushort FujiDynamicRangeSetting;
    ushort FujiDevelopmentDynamicRange;
    ushort FujiAutoDynamicRange;
    ushort FocusMode;
    ushort AFMode;
    ushort FocusPixel[2];
    ushort ImageStabilization[3];
    ushort FlashMode;
    ushort WB_Preset;
    ushort ShutterType;
    ushort ExrMode;
    ushort Macro;
    unsigned Rating;
    ushort FrameRate;
    ushort FrameWidth;
    ushort FrameHeight;
  } libraw_fuji_info_t;

  typedef struct
  {

    double ExposureBracketValue;
    ushort ActiveDLighting;
    ushort ShootingMode;
    /* stabilization */
    uchar ImageStabilization[7];
    uchar VibrationReduction;
    uchar VRMode;
    /* focus */
    char FocusMode[7];
    uchar AFPoint;
    ushort AFPointsInFocus;
    uchar ContrastDetectAF;
    uchar AFAreaMode;
    uchar PhaseDetectAF;
    uchar PrimaryAFPoint;
    uchar AFPointsUsed[29];
    ushort AFImageWidth;
    ushort AFImageHeight;
    ushort AFAreaXPposition;
    ushort AFAreaYPosition;
    ushort AFAreaWidth;
    ushort AFAreaHeight;
    uchar ContrastDetectAFInFocus;
    /* flash */
    char FlashSetting[13];
    char FlashType[20];
    uchar FlashExposureCompensation[4];
    uchar ExternalFlashExposureComp[4];
    uchar FlashExposureBracketValue[4];
    uchar FlashMode;
    signed char FlashExposureCompensation2;
    signed char FlashExposureCompensation3;
    signed char FlashExposureCompensation4;
    uchar FlashSource;
    uchar FlashFirmware[2];
    uchar ExternalFlashFlags;
    uchar FlashControlCommanderMode;
    uchar FlashOutputAndCompensation;
    uchar FlashFocalLength;
    uchar FlashGNDistance;
    uchar FlashGroupControlMode[4];
    uchar FlashGroupOutputAndCompensation[4];
    uchar FlashColorFilter;
    ushort NEFCompression;
    int ExposureMode;
    int nMEshots;
    int MEgainOn;
    double ME_WB[4];
    uchar AFFineTune;
    uchar AFFineTuneIndex;
    int8_t AFFineTuneAdj;
  } libraw_nikon_makernotes_t;

  typedef struct
  {
    int OlympusCropID;
    ushort OlympusFrame[4]; /* upper left XY, lower right XY */
    int OlympusSensorCalibration[2];
    ushort FocusMode[2];
    ushort AutoFocus;
    ushort AFPoint;
    unsigned AFAreas[64];
    double AFPointSelected[5];
    ushort AFResult;
    unsigned ImageStabilization;
    ushort ColorSpace;
    uchar AFFineTune;
    short AFFineTuneAdj[3];
  } libraw_olympus_makernotes_t;

  typedef struct
  {
/* Compression:
 34826 (Panasonic RAW 2): LEICA DIGILUX 2;
 34828 (Panasonic RAW 3): LEICA D-LUX 3; LEICA V-LUX 1; Panasonic DMC-LX1; Panasonic DMC-LX2; Panasonic DMC-FZ30; Panasonic DMC-FZ50;
 34830 (not in exiftool): LEICA DIGILUX 3; Panasonic DMC-L1;
 34316 (Panasonic RAW 1): others (LEICA, Panasonic, YUNEEC);
*/
    ushort Compression;
    ushort BlackLevelDim;
    float BlackLevel[8];
  } libraw_panasonic_makernotes_t;

  typedef struct
  {
    ushort FocusMode;
    ushort AFPointSelected;
    unsigned AFPointsInFocus;
    ushort FocusPosition;
    uchar DriveMode[4];
    short AFAdjustment;
    /*    uchar AFPointMode;     */
    /*    uchar SRResult;        */
    /*    uchar ShakeReduction;  */
  } libraw_pentax_makernotes_t;

  typedef struct
  {
    ushort BlackLevelTop;
    ushort BlackLevelBottom;
    short offset_left, offset_top; /* KDC files, negative values or zeros */
    ushort clipBlack, clipWhite;   /* valid for P712, P850, P880 */
    float romm_camDaylight[3][3];
    float romm_camTungsten[3][3];
    float romm_camFluorescent[3][3];
    float romm_camFlash[3][3];
    float romm_camCustom[3][3];
    float romm_camAuto[3][3];
  } libraw_kodak_makernotes_t;

  typedef struct
  {
    ushort SonyCameraType;
    uchar Sony0x9400_version; /* 0 if not found/deciphered, 0xa, 0xb, 0xc following exiftool convention */
    uchar Sony0x9400_ReleaseMode2;
    unsigned Sony0x9400_SequenceImageNumber;
    uchar Sony0x9400_SequenceLength1;
    unsigned Sony0x9400_SequenceFileNumber;
    uchar Sony0x9400_SequenceLength2;
    libraw_raw_crop_t raw_crop;
    int8_t AFMicroAdjValue;
    int8_t AFMicroAdjOn;
    uchar AFMicroAdjRegisteredLenses;
    ushort group2010;
    ushort real_iso_offset;
    float firmware;
    ushort ImageCount3_offset;
    unsigned ImageCount3;
    unsigned ElectronicFrontCurtainShutter;
    ushort MeteringMode2;
    char SonyDateTime[20];
    uchar TimeStamp[6];
    unsigned ShotNumberSincePowerUp;
  } libraw_sony_info_t;

  typedef struct
  {
    ushort curve[0x10000];
    unsigned cblack[4102];
    unsigned black;
    unsigned data_maximum;
    unsigned maximum;
    long linear_max[4];
    float fmaximum;
    float fnorm;
    ushort white[8][8];
    float cam_mul[4];
    float pre_mul[4];
    float cmatrix[3][4];
    float ccm[3][4];
    float rgb_cam[3][4];
    float cam_xyz[4][3];
    struct ph1_t phase_one_data;
    float flash_used;
    float canon_ev;
    char model2[64];
    char UniqueCameraModel[64];
    char LocalizedCameraModel[64];
    void *profile;
    unsigned profile_length;
    unsigned black_stat[8];
    libraw_dng_color_t dng_color[2];
    libraw_dng_levels_t dng_levels;
    float baseline_exposure;
    int WB_Coeffs[256][4];    /* R, G1, B, G2 coeffs */
    float WBCT_Coeffs[64][5]; /* CCT, than R, G1, B, G2 coeffs */
    libraw_P1_color_t P1_color[2];
  } libraw_colordata_t;

  typedef struct
  {
    enum LibRaw_thumbnail_formats tformat;
    ushort twidth, theight;
    unsigned tlength;
    int tcolors;
    char *thumb;
  } libraw_thumbnail_t;

  typedef struct
  {
    float latitude[3];     /* Deg,min,sec */
    float longtitude[3];   /* Deg,min,sec */
    float gpstimestamp[3]; /* Deg,min,sec */
    float altitude;
    char altref, latref, longref, gpsstatus;
    char gpsparsed;
  } libraw_gps_info_t;

  typedef struct
  {
    float iso_speed;
    float shutter;
    float aperture;
    float focal_len;
    time_t timestamp;
    unsigned shot_order;
    unsigned gpsdata[32];
    libraw_gps_info_t parsed_gps;
    char desc[512], artist[64];
    float FlashEC;
    float FlashGN;
    float CameraTemperature;
    float SensorTemperature;
    float SensorTemperature2;
    float LensTemperature;
    float AmbientTemperature;
    float BatteryTemperature;
    float exifAmbientTemperature;
    float exifHumidity;
    float exifPressure;
    float exifWaterDepth;
    float exifAcceleration;
    float exifCameraElevationAngle;
    float real_ISO;
  } libraw_imgother_t;

  typedef struct
  {
    unsigned greybox[4];   /* -A  x1 y1 x2 y2 */
    unsigned cropbox[4];   /* -B x1 y1 x2 y2 */
    double aber[4];        /* -C */
    double gamm[6];        /* -g */
    float user_mul[4];     /* -r mul0 mul1 mul2 mul3 */
    unsigned shot_select;  /* -s */
    float bright;          /* -b */
    float threshold;       /*  -n */
    int half_size;         /* -h */
    int four_color_rgb;    /* -f */
    int highlight;         /* -H */
    int use_auto_wb;       /* -a */
    int use_camera_wb;     /* -w */
    int use_camera_matrix; /* +M/-M */
    int output_color;      /* -o */
    char *output_profile;  /* -o */
    char *camera_profile;  /* -p */
    char *bad_pixels;      /* -P */
    char *dark_frame;      /* -K */
    int output_bps;        /* -4 */
    int output_tiff;       /* -T */
    int user_flip;         /* -t */
    int user_qual;         /* -q */
    int user_black;        /* -k */
    int user_cblack[4];
    int user_sat; /* -S */

    int med_passes; /* -m */
    float auto_bright_thr;
    float adjust_maximum_thr;
    int no_auto_bright;  /* -W */
    int use_fuji_rotate; /* -j */
    int green_matching;
    /* DCB parameters */
    int dcb_iterations;
    int dcb_enhance_fl;
    int fbdd_noiserd;
    int exp_correc;
    float exp_shift;
    float exp_preser;
    /* Raw speed */
    int use_rawspeed;
    /* DNG SDK */
    int use_dngsdk;
    /* Disable Auto-scale */
    int no_auto_scale;
    /* Disable intepolation */
    int no_interpolation;
    /*  int x3f_flags; */
    /* Sony ARW2 digging mode */
    /* int sony_arw2_options; */
    unsigned raw_processing_options;
    int sony_arw2_posterization_thr;
    /* Nikon Coolscan */
    float coolscan_nef_gamma;
    char p4shot_order[5];
    /* Custom camera list */
    char **custom_camera_strings;
  } libraw_output_params_t;

  typedef struct
  {
    /* really allocated bitmap */
    void *raw_alloc;
    /* alias to single_channel variant */
    ushort *raw_image;
    /* alias to 4-channel variant */
    ushort (*color4_image)[4];
    /* alias to 3-color variand decoded by RawSpeed */
    ushort (*color3_image)[3];
    /* float bayer */
    float *float_image;
    /* float 3-component */
    float (*float3_image)[3];
    /* float 4-component */
    float (*float4_image)[4];

    /* Phase One black level data; */
    short (*ph1_cblack)[2];
    short (*ph1_rblack)[2];
    /* save color and sizes here, too.... */
    libraw_iparams_t iparams;
    libraw_image_sizes_t sizes;
    libraw_colordata_t color;
    ...;
  } libraw_rawdata_t;

  typedef struct
  {
    unsigned long long LensID;
    char Lens[128];
    ushort LensFormat; /* to characterize the image circle the lens covers */
    ushort LensMount;  /* 'male', lens itself */
    unsigned long long CamID;
    ushort CameraFormat; /* some of the sensor formats */
    ushort CameraMount;  /* 'female', body throat */
    char body[64];
    short FocalType; /* -1/0 is unknown; 1 is fixed focal; 2 is zoom */
    char LensFeatures_pre[16], LensFeatures_suf[16];
    float MinFocal, MaxFocal;
    float MaxAp4MinFocal, MaxAp4MaxFocal, MinAp4MinFocal, MinAp4MaxFocal;
    float MaxAp, MinAp;
    float CurFocal, CurAp;
    float MaxAp4CurFocal, MinAp4CurFocal;
    float MinFocusDistance;
    float FocusRangeIndex;
    float LensFStops;
    unsigned long long TeleconverterID;
    char Teleconverter[128];
    unsigned long long AdapterID;
    char Adapter[128];
    unsigned long long AttachmentID;
    char Attachment[128];
    ushort CanonFocalUnits;
    float FocalLengthIn35mmFormat;
  } libraw_makernotes_lens_t;

  typedef struct
  {
    float NikonEffectiveMaxAp;
    uchar NikonLensIDNumber, NikonLensFStops, NikonMCUVersion, NikonLensType;
  } libraw_nikonlens_t;

  typedef struct
  {
    float MinFocal, MaxFocal, MaxAp4MinFocal, MaxAp4MaxFocal;
  } libraw_dnglens_t;

  typedef struct
  {
    float MinFocal, MaxFocal, MaxAp4MinFocal, MaxAp4MaxFocal, EXIF_MaxAp;
    char LensMake[128], Lens[128], LensSerial[128], InternalLensSerial[128];
    ushort FocalLengthIn35mmFormat;
    libraw_nikonlens_t nikon;
    libraw_dnglens_t dng;
    libraw_makernotes_lens_t makernotes;
  } libraw_lensinfo_t;

  typedef struct
  {
    libraw_canon_makernotes_t canon;
    libraw_nikon_makernotes_t nikon;
    libraw_hasselblad_makernotes_t hasselblad;
    libraw_fuji_info_t fuji;
    libraw_olympus_makernotes_t olympus;
    libraw_sony_info_t sony;
    libraw_kodak_makernotes_t kodak;
    libraw_panasonic_makernotes_t panasonic;
    libraw_pentax_makernotes_t pentax;
  } libraw_makernotes_t;

  typedef struct
  {
    short DriveMode;
    short FocusMode;
    short MeteringMode;
    short AFPoint;
    short ExposureMode;
    short ImageStabilization;
    char BodySerial[64];
    char InternalBodySerial[64]; /* this may be PCB or sensor serial, depends on make/model*/
  } libraw_shootinginfo_t;

  typedef struct
  {
    unsigned fsize;
    ushort rw, rh;
    uchar lm, tm, rm, bm, lf, cf, max, flags;
    char t_make[10], t_model[20];
    ushort offset;
  } libraw_custom_camera_t;

  typedef struct
  {
    ushort (*image)[4];
    libraw_image_sizes_t sizes;
    libraw_iparams_t idata;
    libraw_lensinfo_t lens;
    libraw_makernotes_t makernotes;
    libraw_shootinginfo_t shootinginfo;
    libraw_output_params_t params;
    unsigned int progress_flags;
    unsigned int process_warnings;
    libraw_colordata_t color;
    libraw_imgother_t other;
    libraw_thumbnail_t thumbnail;
    libraw_rawdata_t rawdata;
    void *parent_class;
  } libraw_data_t;

  struct fuji_compressed_params
  {
    int8_t *q_table; /* quantization table */
    int q_point[5];  /* quantization points */
    int max_bits;
    int min_value;
    int raw_bits;
    int total_values;
    int maxDiff;
    ushort line_width;
  };

  DllDef const char *libraw_strerror(int errorcode);
  DllDef const char *libraw_strprogress(enum LibRaw_progress);
  /* LibRaw C API */
  DllDef libraw_data_t *libraw_init(unsigned int flags);
  DllDef int libraw_open_file(libraw_data_t *, const char *);
  DllDef int libraw_open_file_ex(libraw_data_t *, const char *, INT64 max_buff_sz);
  DllDef int libraw_open_buffer(libraw_data_t *, void *buffer, size_t size);
  DllDef int libraw_unpack(libraw_data_t *);
  DllDef int libraw_unpack_thumb(libraw_data_t *);
  DllDef void libraw_recycle_datastream(libraw_data_t *);
  DllDef void libraw_recycle(libraw_data_t *);
  DllDef void libraw_close(libraw_data_t *);
  DllDef void libraw_subtract_black(libraw_data_t *);
  DllDef int libraw_raw2image(libraw_data_t *);
  DllDef void libraw_free_image(libraw_data_t *);
  /* version helpers */
  DllDef const char *libraw_version();
  DllDef int libraw_versionNumber();
  /* Camera list */
  DllDef const char **libraw_cameraList();
  DllDef int libraw_cameraCount();

  /* helpers */
  DllDef void libraw_set_memerror_handler(libraw_data_t *, memory_callback cb, void *datap);
  DllDef void libraw_set_exifparser_handler(libraw_data_t *, exif_parser_callback cb, void *datap);
  DllDef void libraw_set_dataerror_handler(libraw_data_t *, data_callback func, void *datap);
  DllDef void libraw_set_progress_handler(libraw_data_t *, progress_callback cb, void *datap);
  DllDef const char *libraw_unpack_function_name(libraw_data_t *lr);
  DllDef int libraw_get_decoder_info(libraw_data_t *lr, libraw_decoder_info_t *d);
  DllDef int libraw_COLOR(libraw_data_t *, int row, int col);
  DllDef unsigned libraw_capabilities();

  /* DCRAW compatibility */
  DllDef int libraw_adjust_sizes_info_only(libraw_data_t *);
  DllDef int libraw_dcraw_ppm_tiff_writer(libraw_data_t *lr, const char *filename);
  DllDef int libraw_dcraw_thumb_writer(libraw_data_t *lr, const char *fname);
  DllDef int libraw_dcraw_process(libraw_data_t *lr);
  DllDef libraw_processed_image_t *libraw_dcraw_make_mem_image(libraw_data_t *lr, int *errc);
  DllDef libraw_processed_image_t *libraw_dcraw_make_mem_thumb(libraw_data_t *lr, int *errc);
  DllDef void libraw_dcraw_clear_mem(libraw_processed_image_t *);
  /* getters/setters used by 3DLut Creator */
  DllDef void libraw_set_demosaic(libraw_data_t *lr, int value);
  DllDef void libraw_set_output_color(libraw_data_t *lr, int value);
  DllDef void libraw_set_user_mul(libraw_data_t *lr, int index, float val);
  DllDef void libraw_set_output_bps(libraw_data_t *lr, int value);
  DllDef void libraw_set_gamma(libraw_data_t *lr, int index, float value);
  DllDef void libraw_set_no_auto_bright(libraw_data_t *lr, int value);
  DllDef void libraw_set_bright(libraw_data_t *lr, float value);
  DllDef void libraw_set_highlight(libraw_data_t *lr, int value);
  DllDef void libraw_set_fbdd_noiserd(libraw_data_t *lr, int value);
  DllDef int libraw_get_raw_height(libraw_data_t *lr);
  DllDef int libraw_get_raw_width(libraw_data_t *lr);
  DllDef int libraw_get_iheight(libraw_data_t *lr);
  DllDef int libraw_get_iwidth(libraw_data_t *lr);
  DllDef float libraw_get_cam_mul(libraw_data_t *lr, int index);
  DllDef float libraw_get_pre_mul(libraw_data_t *lr, int index);
  DllDef float libraw_get_rgb_cam(libraw_data_t *lr, int index1, int index2);
  DllDef int libraw_get_color_maximum(libraw_data_t *lr);

  DllDef libraw_iparams_t *libraw_get_iparams(libraw_data_t *lr);
  DllDef libraw_lensinfo_t *libraw_get_lensinfo(libraw_data_t *lr);
  DllDef libraw_imgother_t *libraw_get_imgother(libraw_data_t *lr);
    """.replace("DllDef ", ""),
)


if __name__ == "__main__":
    ffi.compile()
