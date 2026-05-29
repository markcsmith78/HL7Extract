#!/usr/bin/python3

from hl7_extract import HL7Extract
from logging_setup import setup_logging
from json_validate import validate_config, validate_rules
from output_controller import OutputController
import logging
import argparse
import sys


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
    default="config/config.json",
    help="System configuration file"
)

parser.add_argument(
    "--debug",
    action="store_true",
    help="Enable debug logging"
)


logger = logging.getLogger(__name__)
args = parser.parse_args()

# DON'T access args after this! (except maybe for args.debug)
rules_file = "rules/" + args.rules
input_file = "input/" + args.input
config_file = args.config

if args.debug:
    setup_logging(debug=True)

# system config file
logger.info(f"Using {config_file} as config.")
logger.debug(f"Validaing {config_file} against config.schema.json")
validate_config(config_file, "config.schema.json")

# hl7 rules file
logger.info(f"Using rules_file for rules.")
logger.debug(f"Validaing {rules_file} against rules.schema.json")
validate_rules(rules_file, "rules.schema.json")   

extr = HL7Extract(rules_file, input_file)
el_dict = extr.extract_all_hl7()

outController = OutputController(config_file, el_dict)
outController.printAllElements()

sys.exit(0)
