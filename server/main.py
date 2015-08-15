#!/usr/bin/python2.7
from objects import *

HOST = "192.168.0.50"
PORT = 2222


if __name__ == "__main__":
    Server(HOST, PORT).run()
