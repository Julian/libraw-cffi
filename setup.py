from setuptools import setup
setup(
    cffi_modules=["libraw_cffi/_build.py:ffi"],
    use_scm_version=True,
)
