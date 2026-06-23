import json
import logging
import sys
from abc import ABC, abstractmethod

class HL7InputStream:

    def __init__(self, json_config):
        self._json_config = json_config
        self._raw_file_input = ""

        self.logger = logging.getLogger(__name__)

        self.logger.debug('Initializing HL7InputStream object')

        self._setup_input()
       
    @abstractmethod 
    def _setup_input(self):
        pass

    @abstractmethod
    def get_msg(self):
        pass
    
    @abstractmethod
    def close(self):
        pass

