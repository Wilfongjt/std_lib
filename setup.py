from setuptools import setup, find_packages

from std_lib import __version__

setup(
    name='std_lib',
    version=__version__,
    url='https://github.com/Wilfongjt/std_lib',
    author='James Wilfong',
    author_email='wilfongjt@gmail.com',
    packages=find_packages()
)