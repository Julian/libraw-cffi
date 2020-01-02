# Usage: python examples/save_jpeg_using_pil.py src.CR2 dest.jpg
# Requires PIL (pip install pillow)
import sys

from PIL import Image

from _raw import ffi
from libraw_cffi import Raw


src = sys.argv[1]
dest = sys.argv[2]

raw = Raw.from_path(src)
raw.unpack()
raw.dcraw_process()
processed_image = raw.dcraw_make_mem_image()
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
