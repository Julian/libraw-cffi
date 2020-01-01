# Usage: python examples/save_jpeg_using_pil.py src.CR2 dest.jpg
# Requires PIL (pip install pillow)
import sys

from PIL import Image

from _raw import ffi, lib
import libraw_cffi


src = sys.argv[1]
dest = sys.argv[2]

raw = libraw_cffi.from_path(src)
lib.libraw_unpack(raw)
lib.libraw_dcraw_process(raw)
pointer = ffi.new("int *", 0)
processed_image = lib.libraw_dcraw_make_mem_image(raw, pointer)
rgb_buffer = ffi.buffer(processed_image.data, processed_image.data_size)

image = Image.frombuffer(
    "RGB",
    [processed_image.width, processed_image.height],
    rgb_buffer,
    "raw",
    "RGB",
    0,
    1,
)
image.save(dest)
