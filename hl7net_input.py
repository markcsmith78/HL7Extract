import json
import logging
import sys
import socket
import asyncio
from hl7input_stream import HL7InputStream

class HL7NetInput(HL7InputStream):

    def get_msg(self):
        
        MLLP_START = b"\x0b"
        MLLP_END = b"\x1c\x0d"
    
        conn, addr = self.server_socket.accept()
        self.logger.debug("Accepted connection from %s", addr)
    
        buffer = bytearray()
    
        try:
            while MLLP_END not in buffer:
                chunk = conn.recv(4096)
    
                if not chunk:
                    raise ConnectionError(
                        "Connection closed before complete MLLP message was received"
                    )
    
                buffer.extend(chunk)
    
            start_index = buffer.find(MLLP_START)
            end_index = buffer.find(MLLP_END)
    
            if start_index == -1:
                raise ValueError("MLLP start character not found")
    
            message_bytes = buffer[start_index + 1:end_index]
    
            self._hl7_msg = message_bytes.decode("utf-8")
    
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

