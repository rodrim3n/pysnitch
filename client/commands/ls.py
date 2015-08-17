import os


def run(*args):
    output = os.listdir(args[0]) if args[0] else os.listdir('.')
    return ' '.join(output)
