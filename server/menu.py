# -*- coding: utf-8 -*-

import os
import sys

from cmd import Cmd
from tabulate import tabulate


class Shell(Cmd):

    def __init__(self, client):
        Cmd.__init__(self)
        self.client = client
        self.prompt = self.client.username+'@'+self.client.address[0] + " $ "
        self.intro = 'Mensaje introductorio.'

    def do_clear(self, arg):
        os.system("clear")

    def do_exit(self, arg):
        return True

    def default(self, arg):
        input_command = self.command_parser(self.lastcmd)
        self.client.send(input_command)
        received = self.client.recv()
        print(received)

    def command_parser(self, command):
        ret = self.parseline(command)
        command = ';'.join(list(ret)[0:2])
        return command


class Menu(object):

    def __init__(self, server):
        self.server = server
        self.menu_actions = {
            'main_menu': self.main_menu,
            '1': self.show_connections,
            '2': self.choose_client,
            '9': self.back,
            '0': self.exit,
        }

    def main_menu(self):
        print("1. Show Connections")
        print("2. Choose Client")
        print("0. Quit")
        choice = input(">>  ")
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
                print("Invalid selection, please try again.\n")
                self.menu_actions['main_menu']()
                return

    def show_connections(self):
        os.system('clear')
        print("Connections !")
        table = self.server.refresh_connections()
        print(tabulate(table, headers=['Index', 'Name', 'Addr'],
                       tablefmt='psql'))
        self.back()

    def choose_client(self):
        print("Choose Client !")
        choice = input(">>  ")
        client = self.server.search_client(choice)
        if client:
            Shell(client).cmdloop()
        else:
            os.system('clear')
            print("Invalid selection, please try again.\n")
            self.show_connections()
            self.back()

    def back(self):
        self.menu_actions['main_menu']()

    def exit(self):
        self.server.close_connections()
        sys.exit()
