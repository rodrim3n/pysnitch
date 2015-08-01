#!/usr/bin/python2.7
from objects import *

HOST = "192.168.0.50"
PORT = 2222


def main():
    Server(HOST, PORT).run()

if __name__ == "__main__":
    main()
