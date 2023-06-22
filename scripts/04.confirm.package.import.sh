#!/bin/sh
cd ..
#python3 -c "import std_lib; std_lib.hello_world()"
#python3 -c "from std_lib import hello_world; hello_world()"

python3 -c "from std_lib.greetings import hello_world; hello_world()"

python3 -c "from std_lib.math import add; print(add(1, 3))"
