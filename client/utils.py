# -*- coding: utf-8 -*-

from contextlib import suppress


class RequestParser(object):

    def __init__(self, request, delimiter=';'):
        try:
            self.delimiter = delimiter
            self.command, self.args = self._parse_request(request)
            self.is_valid = True if self.command else False
        except ValueError:
            self.is_valid = False

    def _parse_request(self, request):
        return request.split(self.delimiter)[0:2]


def windows_setup():
    with suppress(Exception):
        import _winreg
        key = _winreg.OpenKey(
            _winreg.HKEY_CURRENT_USER,
            'Software\Microsoft\Windows\CurrentVersion\Run',
            0, _winreg.KEY_SET_VALUE
        )

        _winreg.SetValueEx(
            key, 'ptest', 0, _winreg.REG_SZ, "C:\Python27\Scripts\main.lnk")

        key.Close()
