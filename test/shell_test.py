import unittest
from server.objects import *


class TestShell(unittest.TestCase):

    def setUp(self):
        self.client = ClientConnection('socket', 'adress', 'username')
        self.shell = Shell(self.client)

    def test_command_parser_no_args(self):
        cmd = 'ls'
        self.assertEqual('ls;', self.shell.command_parser(cmd))

    def test_command_parser_single_arg(self):
        cmd = 'ls /home'
        self.assertEqual('ls;/home', self.shell.command_parser(cmd))

    def test_command_parser_multiple_args(self):
        cmd = 'ls /home /pepe /asd'
        self.assertEqual('ls;/home /pepe /asd', self.shell.command_parser(cmd))


if __name__ == '__main__':
    unittest.main()
