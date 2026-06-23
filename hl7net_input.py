import json
import logging
import sys
import socket
import asyncio
from hl7input_stream import HL7InputStream

class HL7NetInput(HL7InputStream):

    def get_msg(self):
        
        conn, addr = self.server_socket.accept()

        self.logger.debug("Accepted connection from %s", addr)

        try: 
            #msg = b""
        
            #while b"\x1c\x0d" not in msg:
            msg = conn.recv(1024)

            #    if not chunk: 
            #        break

            #    msg += chunk

            #msg = msg.lstrip(b"\x0b").rstrip(b"\x1c\x0d")
            self._hl7_msg = msg.decode("utf-8")

            self.logger.debug("Received %s", self._hl7_msg)

            return self._hl7_msg

        finally:
            conn.close() 

    def _setup_input(self):
        self._host = self._json_config['input']['host']
        self._port = self._json_config['input']['port']
    
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self._host, self._port))
        self.server_socket.listen()

        self.logger.debug("Server listening on %s:%s", self._host, self._port)  

    def close(self):
        self.server_socket.close()

