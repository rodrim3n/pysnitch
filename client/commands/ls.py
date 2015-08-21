import os


def run(*args):
    try:
        output = os.listdir(args[0]) if args[0] else os.listdir('.')
        return ' '.join(output)
    except:
        return 'Invalid path.'
