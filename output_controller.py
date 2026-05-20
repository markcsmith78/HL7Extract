import logging
import sys

#superclass for output subclasses.  defines the interface that
#subclasses override to create polymorphic relationship
class OutPutController: 

    def __init__(self, config_file, hl7_dict):
       
        # open & process JSON rules 
        try: 
            with open(json_file) as ifile:
                self.config_json = json.load(ifile)
        except FileNotFoundError:
            self.logger.critical(f"Config file not found: {json_file}.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            self.logger.critical(f"Invalid JSON: {e}")
            sys.exit(1)

 
