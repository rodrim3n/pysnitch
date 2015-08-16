#!/usr/bin/python2.7
from objects import *
import sys
import getopt

# This script can receive a host and a port -> 'h:p:'

try:
    options = getopt.getopt(sys.argv[1:], 'h:p:')
    options = dict(options[0])
except:
    print 'Wrong arguments received, defaulting to localhost:2222'
    options = {}

default_options = {'-h': '0.0.0.0', '-p': 2222}

# Merge received arguments with default ones
options = dict(default_options, **options)

HOST = options['-h']
PORT = options['-p']

if __name__ == "__main__":
    Server(HOST, PORT).run()
