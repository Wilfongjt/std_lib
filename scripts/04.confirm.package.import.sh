#!/bin/sh
cd ..
#python3 -c "import std_lib_package; std_lib_package.hello_world()"
#python3 -c "from std_lib_package import hello_world; hello_world()"

python3 -c "from std_lib_package.greetings import hello_world; hello_world()"

python3 -c "from std_lib_package.math import add; print(add(1, 3))"
