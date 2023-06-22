#!/bin/sh
cd ..
## Syntax: pip install "Package" @ git+"URL of the repository"
## eg pip install pip@git+https://github.com/pypa/pip
pip install std_lib@git+https://github.com/Wilfongjt/std_lib

#pip install git+https://github.com/Wilfongjt/std_lib.git#egg=my_pip_package
#pip install git+git://github.com/Wilfongjt/std_lib.git#egg=my_pip_package