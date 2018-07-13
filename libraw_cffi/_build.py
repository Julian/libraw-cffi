from cffi import FFI


ffi = FFI()


ffi.set_source(
    "_raw",
    '#include "libraw/libraw.h"',
    libraries=["raw"],
)

ffi.cdef(
    """
    typedef unsigned short ushort;

    typedef struct
        {
        char	    guard[4];
        char        make[64];
        char        model[64];
        char        software[64];
        unsigned    raw_count;
        unsigned    dng_version;
        unsigned    is_foveon;
        int         colors;
        unsigned    filters;
        char        xtrans[6][6];
        char        xtrans_abs[6][6];
        char        cdesc[5];
        unsigned    xmplen;
        char        *xmpdata;
    } libraw_iparams_t;

    typedef struct { ...; } libraw_colordata_t;
    typedef struct { ...; } libraw_imgother_t;
    typedef struct { ...; } libraw_lensinfo_t;
    typedef struct { ...; } libraw_makernotes_t;
    typedef struct { ...; } libraw_shootinginfo_t;
    typedef struct { ...; } libraw_thumbnail_t;

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

    libraw_data_t *libraw_init(unsigned int flags);
    int libraw_open_file(libraw_data_t *, const char *);
    int libraw_unpack(libraw_data_t *);
    void libraw_recycle(libraw_data_t *);
    int libraw_raw2image(libraw_data_t *);
    """,
)


if __name__ == "__main__":
    ffi.compile()
