import socket
import commands
import time


class Client:

    def __init__(self, host, port):
        self.socket = None
        self.port = port
        self.host = host

    def run(self):
        self.connect_server()
        while True:
            request = RequestParser(self.socket.recv(4096))

            if request.is_valid:
                command = self.fetch_command(request.command)
                response = command.run(request.args)
                self.socket.sendall(response)
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

    def fetch_command(self, command_name):
        return getattr(commands, command_name)


class RequestParser:

    def __init__(self, request, delimiter=';'):
        try:
            self.delimiter = delimiter
            self.command, self.args = self._parse_request(request)
            self.is_valid = True if self.command else False
        except ValueError:
            self.is_valid = False

    def _parse_request(self, request):
        return request.split(self.delimiter)


