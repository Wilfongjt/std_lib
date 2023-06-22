from setuptools import setup

from std_lib_package import __version__

setup(
    name='std_lib_package',
    version=__version__,

    url='https://github.com/Wilfongjt/std_lib',
    author='James Wilfong',
    author_email='wilfongjt@gmail.com',

    py_modules=['std_lib_package']
)