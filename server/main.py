#!/usr/bin/python3
import uuid

HOST = socket.gethostname()
PORT = 2222


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
            received = client[0].recv(4096).decode("UTF-8")
            print(received)





def main():


if __name__ == "__main__":
    main()
