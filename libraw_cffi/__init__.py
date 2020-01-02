try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata
__version__ = metadata.version("libraw_cffi")

from libraw_cffi._api import (
    LibRawError,
    Raw,
    version,
    version_info,
)
