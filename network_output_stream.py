import logging
from output_stream import OutputStream

#extends OutputStream to create a class-specific implementation of send_output()
class NetworkOutputStream(OutputStream):
    
    def __init__(self, o_config, hl7dict):
        self.hl7_dict = hl7dict
        self.out_config = o_config

        self.logger = logging.getLogger(__name__)

    def send_output(self):

        self.logger.debug("Using network output: ") 
     
