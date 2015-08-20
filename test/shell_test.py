import unittest
from server.objects import *


class TestShell(unittest.TestCase):

    def setUp(self):
        self.client = 'client'
        self.shell = Shell(self.client)

    def test_command_adds_no_args(self):
        cmd = 'ls'
        self.assertEqual('ls;', self.shell.command_adds(cmd))

    def test_command_adds_with_args(self):
        cmd = 'ls /home'
        self.assertEqual('ls;/home;', self.shell.command_adds(cmd))


if __name__ == '__main__':
    unittest.main()
