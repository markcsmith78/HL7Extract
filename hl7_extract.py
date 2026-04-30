#!/usr/bin/python3

import json
import hl7

class HL7Extract:

    def __init__(self, json_file, hl7_file):
        self.hl7_value = []
        
        try: 
            with open(json_file) as ifile:
                self.nssp_json = json.load(ifile)
        except FileNotFoundError:
            print("File not found.")
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}")

        try:
            with open(hl7_file, "r") as ifile:
                msg = ifile.read()
        except FileNotFoundError:
            print(f"ERROR: File not found {file_path}.")

        msg = msg.replace('\r\n', '\r').replace('\n', '\r')
        self.hl7_msg = hl7.parse(msg)

    def extract_field(self, el):
    
        if isinstance(self.hl7_msg[el['segment']][el['segment_repetition']][el['field']][el['field_repetition']], list):
            return '^'.join(self.flatten_strings(self.hl7_msg[el['segment']][el['segment_repetition']][el['field']][el['field_repetition']]))
        else:
            return self.hl7_msg[el['segment']][el['segment_repetition']][el['field']][el['field_repetition']]

    def extract_component(self, el):

        #TODO: manage repeating components, subcomponents
        #if isinstance(self.hl7_msg[el['segment']][el['segment_repetition']][el['field']][el['field_repetition']], list):
            return self.hl7_msg[el['segment']][el['segment_repetition']][el['field']][el['field_repetition']][el['component']][el['subcomponent']]


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

            print(f'Name: {el["name"]}')
            for src in el['source']: 

                print(f"\tNotation: {src['notation']}")
                print(f"\t[{src['segment']}][{src['segment_repetition']}][{src['field']}][{src['field_repetition']}][{src['component']}][{src['subcomponent']}]")
                # FIELD only
                if src['component'] == 0:
                    extract = self.extract_field(src) 
                # COMPONENT
                else: 
                    extract = self.extract_component(src)

                ret_list[el['name']] = extract 

        return ret_list
        
    
