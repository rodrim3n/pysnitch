#!/usr/bin/env python

import json

import utils
from client import Client

utils.windows_setup()

with open('client_config.json', 'r') as f:
    config = json.loads(f.read())
    HOST = config.get('HOST')
    PORT = config.get('PORT')

assert HOST, "Host must be assigned."
assert PORT, "Port must be assigned."


if __name__ == "__main__":
    Client(HOST, PORT).run()
