#!/usr/bin/python3

# rename_to_hash.py
# Rename a file to its hash, while keeping its extension, as long as it's a
# "single" extension, so ".png" will be kept, but ".tar.gz" will be changed
# into ".gz".

import os
import sys

files = sys.argv
files.pop(0)

if len(files) <= 0:
    print("No arguments given.")
    sys.exit(-1)

for filename in files:
    filehash = os.popen("sha1sum " + filename).read().split(' ')[0]
    extension = filename.split('.')[-1]

    new_filename = filehash + "." + extension

    mvcmd = "mv " + filename + " " + new_filename
    print(mvcmd)
    os.popen(mvcmd)
