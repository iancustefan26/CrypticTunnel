from setuptools import  setup, Extension
import pybind11
import sysconfig

include_dirs = [
    pybind11.get_include(),
    sysconfig.get_paths()["include"],
    "/opt/homebrew/opt/openssl@3/include"
]

library_dirs = [
    "/opt/homebrew/opt/openssl@3/lib"
]

libraries = [
    "ssl", "crypto"
]

ext_modules = [
    Extension(
        'rsalib',  
        ['crypto.cpp'], 
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        language='c++',
        extra_compile_args=['-std=c++11'], 
    ),
]

setup(
    name='rsalib',
    version='0.1',
    ext_modules=ext_modules,
)