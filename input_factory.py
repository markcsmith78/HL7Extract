import json
import logging
import sys
from hl7file_input import HL7FileInput
#from hl7net_input import HL7NetInput

class InputFactory: 
    
    @classmethod
    def create(cls, j_config):

        logger = logging.getLogger(__name__)

        match j_config['input']['type']:
            case "file":
                logger.debug(f'Using file {j_config["input"]["path"]} as input')
                return HL7FileInput(j_config)
            case "network":     
                self.logger.debug(f'Using {j_config["input"]["host"]}:{j_config["input"]["port"]} as input')
            case _:
                self.logger.critical('Unexpected output specified.  Exiting.')
                sys.exit(1)  
