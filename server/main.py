#!/usr/bin/python3
from objects import *

HOST = socket.gethostname()
PORT = 2222


def main():
    Server(HOST, PORT).run()

if __name__ == "__main__":
    main()
