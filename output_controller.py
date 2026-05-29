import logging
import sys
import json
from terminal_output_stream import TerminalOutputStream
from network_output_stream import NetworkOutputStream
from csv_output_stream import CSVOutputStream

#'Controller' class used to instantiate OutputStream subclasse objects
class OutputController: 

    def __init__(self, config_file, hl7_dict):

        self.logger = logging.getLogger(__name__)
        self.element_dict = hl7_dict

        #keys are from .json config 
        self.output_classes = {'terminal': TerminalOutputStream,
                               'csv': CSVOutputStream,
                               'network': NetworkOutputStream}
        #objects created from above classes
        self.output_destinations = []
       
        # open & process JSON rules 
        try: 
            with open(config_file) as ifile:
                self.config_json = json.load(ifile)
        except FileNotFoundError:
            self.logger.critical(f"Config file not found: {json_file}.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            self.logger.critical(f"Invalid JSON: {e}")
            sys.exit(1)

    def printAllElements(self):

        self.logger.debug("output_controller:printAllElements()")
        
        #crate objects for each destination
        for json_destination in self.config_json["output"]["destinations"]:
            if json_destination['enabled'] == True:
                self.logger.debug(f'Creating: {json_destination["type"]} object...')
                # create output object in our output_destinations array, pass the LOCAL json configuration
                # object so the output destination obj knows how to configure itself
                self.output_destinations.append(self.output_classes[json_destination['type']](json_destination, self.element_dict))

        for output_destination in self.output_destinations:
            output_destination.send_output() 
 
 
