import json
import logging
import sys
from hl7input_stream import HL7InputStream

class HL7FileInput(HL7InputStream):
        
    def _setup_input(self):

        self.logger.debug("Initializing input file...")
        try:
	        with open(self._json_config['input']['path'], "r") as ifile:
	            self._raw_file_input = ifile.read()
        except FileNotFoundError:
            self.logger.critical(f'ERROR: File not found {json_config["input"]["path"]}')
            sys.exit(1)

        # take care of carriage returns, newlines...
        self._raw_file_input = self._raw_file_input.replace('\r\n', '\r').replace('\n', '\r')

        # break down the raw input into individual hl7 messages
        self._split_mllp_messages()
    
    def _split_mllp_messages(self):
	    MLLP_START = b'\x0b'.decode()
	    MLLP_END = b'\x1c'.decode() + b'\x0d'.decode()
	
	    self._msg_list = []
	
	    raw_data = self._raw_file_input
	
	    while True:
	        start_index = raw_data.find(MLLP_START)
	        if start_index == -1:
	            break
	        end_index = raw_data.find(MLLP_END, start_index)
	        if end_index == -1:
	            break
	        message = raw_data[start_index + 1:end_index]
	        self._msg_list.append(message)
	        raw_data = raw_data[end_index + len(MLLP_END):] 

    def get_msg(self):
        if self._msg_list:
            return self._msg_list.pop()
        else:
            return "" 

    # this method is really for awaitable i/o operations like networking, but 
    # I need to extend it, so here it is
    def close(self):
        pass         

