#!/usr/bin/python3

import json
import hl7
import logging
import sys

class HL7Extract:

    def __init__(self, json_file, hl7_file):
        self.hl7_value = []

        # system
        self.logger = logging.getLogger(__name__)
       
        # open & process JSON config 
        try: 
            with open(json_file) as ifile:
                self.nssp_json = json.load(ifile)
        except FileNotFoundError:
            self.logger.critical(f"File not found: {json_file}.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            self.logger.critical(f"Invalid JSON: {e}")
            sys.exit(1)

        # open & process hl7 input
        try:
            with open(hl7_file, "r") as ifile:
                msg = ifile.read()
        except FileNotFoundError:
            self.logger.critical(f"ERROR: File not found {hl7_file}.")
            sys.exit(1)

        msg = msg.replace('\r\n', '\r').replace('\n', '\r')
        self.hl7_msg = hl7.parse(msg)



    def extract_field(self, el):
        if isinstance(self.hl7_msg[el['segment']][el['segment_repetition']][el['field']][el['field_repetition']], list):
            return '^'.join(self.flatten_strings(self.hl7_msg[el['segment']][el['segment_repetition']][el['field']][el['field_repetition']]))
        else:
            return self.hl7_msg[el['segment']][el['segment_repetition']][el['field']][el['field_repetition']]

    def extract_component(self, el):
        #TODO: test components, subcomponents
        component = el['component'] - 1 
        return self.hl7_msg[el['segment']][el['segment_repetition']][el['field']][el['field_repetition']][component][el['subcomponent']]


    def flatten_strings(self, data):
        for item in data: 
            if isinstance(item, list):
                yield from self.flatten_strings(item)
            else:
                yield item


    def extract_all_hl7(self):
        ret_list = {}
	    # Notes: 
	    # 1) Repeating segments will be represented by the following notation:
	    #    <SEG>[repetition #]-<field>... (ex.  OBX[3]-2 )
	    # 2) Fields are accessed w/ 1-based indexing, everything else is 0 
	    # 3) If the user denoted field access (i.e. PV1-44), the entire
	    #    field is returned with all components 
	    # 4) If the user denotes the first component in a field (ex. DG1-3.1), there HAS to 
	    #    be at least 2 components in the field -- it will not return the entire field as 
	    #    the only component  (see #3)
        
        for el in self.nssp_json:
        #TODO: add propper debugging 
            #print(f'Name: {el["name"]}')
            for src in el['source']: 

                self.logger.debug(f"\tNotation: {src['notation']}")
                self.logger.debug(f"\t[{src['segment']}][{src['segment_repetition']}][{src['field']}][{src['field_repetition']}][{src['component']}][{src['subcomponent']}]")
                # FIELD only
                if src['component'] == 0:
                    extract = self.extract_field(src) 
                # COMPONENT
                else: 
                    extract = self.extract_component(src)

                ret_list[el['name']] = extract 

        return ret_list
        
    
