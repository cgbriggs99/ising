#!/usr/bin/python3

import os
import re
import sys
import shutil

build_dirs = os.listdir("build")
lib_dir = next(filter(lambda x: re.match("lib\\..*", x), build_dirs))
files = os.listdir("build/" + lib_dir)
modfile = next(filter(lambda x: re.match("fastc\\..*\\..*", x), files))
parts = modfile.split(".")
shutil.copyfile("build/" + lib_dir + "/" + modfile, "ising/" + parts[0] + "."
                + parts[-1])
shutil.copyfile("build/" + lib_dir + "/" + modfile, "ising/" + modfile)
