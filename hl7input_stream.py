import json
import logging
import sys

class HL7InputStream:

    def __init__(self, json_config):
        self._json_config = json_config
        self._raw_file_input = ""

        self.logger = logging.getLogger(__name__)

        self.logger.debug('Initializing HL7InputStream object')

        self._setup_input()
        
    def get_msg(self):
        raise NotImplementedError("Subclasses must implement output()")

    def _setup_input(self):
        raise NotImplementedError("Subclasses must implement output()")
    
