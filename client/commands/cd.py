import os
from commands import pwd


def run(*args):
    try:
        os.chdir(args[0]) if args[0] else os.listdir('..')
        return pwd.run()
    except:
        return 'Invalid path.'
