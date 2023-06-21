from setuptools import setup

from my_pip_package import __version__

setup(
    name='my_pip_package',
    version=__version__,

    url='https://github.com/Wilfongjt/std_lib',
    author='James Wilfong',
    author_email='wilfongjt@gmail.com',

    py_modules=['my_pip_package'],
)