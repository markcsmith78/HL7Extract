#!/usr/bin/python3

from hl7_extract import HL7Extract
from logging_setup import setup_logging
import sys
import logging
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--input", 
    required=True,
    help="Input HL7 file"
)

parser.add_argument(
    "--rules",
    required=True,
    help="Extraction rules JSON file"
)

parser.add_argument(
    "--config",
    default="config.json",
    help="System configuration file"
)

parser.add_argument(
    "--debug",
    action="store_true",
    help="Enable debug logging"
)

logger = logging.getLogger(__name__)
args = parser.parse_args()

if args.debug:
    setup_logging(debug=True)

#not actually using config yet, but this provides
#the scaffolding for when we do
if args.config:
    logger.info(f"Using {args.config} as config.")
    extr = HL7Extract(args.rules, args.input)
else: 
    logger.info("Using config.json as config.")
    extr = HL7Extract(args.rules, args.input)
    
ret = extr.extract_all_hl7()

if args.debug:
    for key in ret:
        logger.debug(f"{key} -> {ret[key]}")

sys.exit(0)
