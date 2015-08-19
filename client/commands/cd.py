import os
import pwd


def run(*args):
    try:
        output = os.chdir(args[0]) if args[0] else os.listdir('..')
        return pwd.run()
    except:
        return 'Invalid path.'

