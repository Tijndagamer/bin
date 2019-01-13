#!/usr/bin/python3

# rename_to_hash.py
# Rename a file to its hash, while keeping its extension, as long as it's a
# "single" extension, so ".png" will be kept, but ".tar.gz" will be changed
# into ".gz".

import os
import sys

filename = sys.argv[1]
print(filename)

filehash = os.popen("sha1sum " + filename).read().split(' ')[0]
extension = filename.split('.')[-1]
print(filehash)

new_filename = filehash + "." + extension
print(new_filename)

mvcmd = "mv " + filename + " " + new_filename
print(mvcmd)
os.popen(mvcmd)
