# -*- coding: utf-8 -*-

import socket
import commands
import time
from utils import RequestParser


class Client(object):

    def __init__(self, host, port):
        self.socket = None
        self.port = port
        self.host = host

    def run(self):
        self.connect_server()
        while True:
            request = RequestParser(self.socket.recv(4096).decode('utf-8'))

            if request.is_valid:
                output = self.exec_command(request.command, request.args)
                self.socket.sendall(output.encode('utf-8'))
            else:
                print("Connection lost.")  # TODO: log shite
                self.connect_server()

    def connect_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False
        while not connected:
            try:
                self.socket.connect((self.host, self.port))
                connected = True
                print("Connected.")
            except socket.error:
                print("Trying to connect...")
                time.sleep(1)

    def exec_command(self, command_name, command_args):
        if hasattr(commands, command_name):
            output = getattr(commands, command_name).run(command_args)
        else:
            output = 'Unknown command.'
        return output
