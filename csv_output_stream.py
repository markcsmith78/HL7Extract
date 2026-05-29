import logging
import csv
from output_stream import OutputStream

#extends OutputStream to create a class-specific implementation of send_output()
class CSVOutputStream(OutputStream):
    
    def __init__(self, o_config, hl7dict):
        self.hl7_dict = hl7dict
        self.out_config= o_config

        self.logger = logging.getLogger(__name__)

        self.logger.debug(f'Using {self.out_config["path"]} as csv output file.')



    def send_output(self):
        headers = []
        out_arr = []
        self.logger.debug("Using CSV output: ") 
        
        for key in self.hl7_dict:
            headers.append(key)
            out_arr.append(self.hl7_dict[key])

        try: 
            with open(self.out_config['path'], 'w', newline='') as ofile:
                csv_writer = csv.writer(ofile)
                csv_writer.writerow(headers)
                csv_writer.writerow(out_arr) 
        except OSError as e:
            print(f'File error: {e}')


        
     
