import json
import hl7
import logging
import sys
from hl7input_stream import HL7InputStream
from input_factory import InputFactory

class HL7Extract:
    
    # json files shall have the absolute file path
    def __init__(self, j_rules, j_config):
        # holds the raw hl7 msg string
        self._raw_hl7_msg = ""
        # holds the dictionary containing all the elements pulled from the above
        self._parsed_hl7_msg = {}
        # holds select elements form the above
        self._extracted_elements = {}

        # system
        self.logger = logging.getLogger(__name__)
       
        # open & process JSON rules 
        try: 
            with open(j_rules) as ifile:
                self.json_rules = json.load(ifile)
        except FileNotFoundError:
            self.logger.critical(f"File not found: {j_rules}.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            self.logger.critical(f"Invalid JSON: {e}")
            sys.exit(1)

        # open & process JSON config 
        try: 
            with open(j_config) as ifile:
                self.json_config = json.load(ifile)
        except FileNotFoundError:
            self.logger.critical(f"File not found: {j_config}.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            self.logger.critical(f"Invalid JSON: {e}")
            sys.exit(1)

        # setup our input stream
        self.input_stream = InputFactory.create(self.json_config)
    
    def _extract_field(self, el):
        if isinstance(self._parsed_hl7_msg[el['segment']][el['segment_repetition']][el['field']][el['field_repetition']], list):
            return '^'.join(self._flatten_strings(self._hl7_msg[el['segment']][el['segment_repetition']][el['field']][el['field_repetition']]))
        else:
            return self._parsed_hl7_msg[el['segment']][el['segment_repetition']][el['field']][el['field_repetition']]

    def _extract_component(self, el):
        #TODO: test components, subcomponents
        component = el['component'] - 1 
        return self._parsed_hl7_msg[el['segment']][el['segment_repetition']][el['field']][el['field_repetition']][component][el['subcomponent']]


    def _flatten_strings(self, data):
        for item in data: 
            if isinstance(item, list):
                yield from self._flatten_strings(item)
            else:
                yield item

    # returns dictionary of 'notation' -> 'hl7 element' entries
    def _extract_elements(self):
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
        
        for el in self.json_rules:
        #TODO: add propper debugging 
            #print(f'Name: {el["name"]}')
            for src in el['source']: 

                self.logger.debug(f"\tNotation: {src['notation']}")
                self.logger.debug(f"\t[{src['segment']}][{src['segment_repetition']}][{src['field']}][{src['field_repetition']}][{src['component']}][{src['subcomponent']}]")
                # FIELD only
                if src['component'] == 0:
                    extract = self._extract_field(src) 
                # COMPONENT
                else: 
                    extract = self._extract_component(src)

                ret_list[el['name']] = extract 

        return ret_list
        
    def get_elements(self):

        self.logger.debug("Parsing msg...")

        self._raw_hl7_msg = self.input_stream.get_msg()
        
        #normalize newlines into carriage returns
        self._raw_hl7_msg = self._raw_hl7_msg.replace("\n\r", "\r")
        self._raw_hl7_msg = self._raw_hl7_msg.replace("\n", "\r")

        # if the input stream is dry, return an empty string
        if (self._raw_hl7_msg == ""):
            return ""
        else: 
            #for segment in self._raw_hl7_msg.split('\r'):
            #   self.logger.debug(segment)

            self._parsed_hl7_msg = hl7.parse(self._raw_hl7_msg)
	        
            self._extracted_elements = self._extract_elements()
            return self._extracted_elements 

