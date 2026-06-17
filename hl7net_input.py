import json
import logging
import sys
import socket
from hl7input_stream import HL7InputStream

class HL7NetInput(HL7InputStream):

    def get_msg(self):
        # this will block until a connection is made, obviously
        # it isn't permanent 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(("127.0.0.1", 5000))
            server_socket.listen()

            conn, addr = server_socket.accept()

            raw_msg = conn.recv(1024)
            self.hl7_msg = raw_msg.decode('utf-8')

            self.logger.debug('Received %s', self.hl7_msg)
            self.logger.debug('Server listening')
            return self.hl7_msg

    def _setup_input(self):
        pass
    
    
