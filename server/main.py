#!/usr/bin/env python

import sys
import getopt

from server import Server

# This script can receive a host and a port -> 'h:p:'

try:
    options = getopt.getopt(sys.argv[1:], 'h:p:')
    options = dict(options[0])
except:
    print('Wrong arguments received, defaulting to localhost:2222')
    options = {}


def merge_options(options):
    '''Merge received arguments with default ones'''

    default_options = {'-h': '0.0.0.0', '-p': 2222}
    return dict(default_options, **options)


if __name__ == "__main__":
    options = merge_options(options)
    HOST = options['-h']
    PORT = options['-p']
    Server(HOST, PORT).run()
