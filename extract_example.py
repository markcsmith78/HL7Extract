#!/usr/bin/python3

from hl7_extract import HL7Extract

extr = HL7Extract("p1_nodups.json", "ex1.hl7")
ret = extr.extract_all_hl7()

for key in ret:
    print(f"{key}: {ret[key]}")

