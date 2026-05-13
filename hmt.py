#!/usr/bin/python3
# This script provides a way to debug and analyze the
# python hl7 library and the hl7 structure it returns

import hl7
import sys

if len(sys.argv) < 2:
    print("Usage: hmt.py <file.hl7>")
    sys.exit(1)

try:
    with open(sys.argv[1], "r") as ifile:
        msg = ifile.read()
except FileNotFoundError:
    print(f"ERROR: File not found {file_path}.")

msg = msg.replace('\r\n', '\r').replace('\n', '\r')
hl7_msg = hl7.parse(msg)

#put a breakpoint on the following line, then use pdb to
#mess around w/ hl7_msg and get a better appreciation of 
#how it stores hl7 data
print("done")

