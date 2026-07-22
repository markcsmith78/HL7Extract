import json
import logging
import sys
import socket
import asyncio
from hl7input_stream import HL7InputStream

class HL7NetInput(HL7InputStream):

    def __init__(self, json_config):
        super().__init__(json_config)

        self._connection = None
        self._connection_address = None
        self._receive_buffer = bytearray()

    def get_msg(self):
            
        MLLP_START = b"\x0b"
        MLLP_END = b"\x1c\x0d"
    
        buffer = self._receive_buffer
    
        while True:
    
            if self._connection is None:
                self._connection, self._connection_address = (
                    self.server_socket.accept()
                )
    
                self.logger.debug(
                    "Accepted connection from %s",
                    self._connection_address,
                )
    
            while MLLP_END not in buffer:
                chunk = self._connection.recv(4096)
    
                if not chunk:
                    self._connection.close()
                    self._connection = None
                    self._connection_address = None
    
                    if buffer:
                        buffer.clear()
    
                        raise ConnectionError(
                            "Connection closed before complete MLLP message was received"
                        )
    
                    break
    
                buffer.extend(chunk)
    
            if self._connection is None:
                continue
    
            start_index = buffer.find(MLLP_START)
    
            if start_index == -1:
                buffer.clear()
                raise ValueError("MLLP start character not found")
    
            end_index = buffer.find(
                MLLP_END,
                start_index + len(MLLP_START),
            )
    
            if end_index == -1:
                continue
    
            message_bytes = buffer[
                start_index + len(MLLP_START):end_index
            ]
    
            del buffer[:end_index + len(MLLP_END)]
    
            self._hl7_msg = message_bytes.decode("utf-8")
    
            self.logger.debug(
                "Received %s",
                self._hl7_msg,
            )
    
            return self._hl7_msg

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

