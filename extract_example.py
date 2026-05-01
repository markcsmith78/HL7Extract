#!/usr/bin/python3

from hl7_extract import HL7Extract
import sys

if len(sys.argv) < 3:
   print("Usage: hl7_extract <config.json> <msg.hl7>")
   sys.exit(1)

extr = HL7Extract(sys.argv[1], sys.argv[2])
ret = extr.extract_all_hl7()

for key in ret:
    print(f"{key} -> {ret[key]}")

