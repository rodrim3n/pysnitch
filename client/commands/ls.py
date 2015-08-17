import os

def run(*args):
    return os.listdir(args[0]) if args[0] else os.listdir('.')
