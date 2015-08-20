import unittest
from server.main import *


class TestServerScript(unittest.TestCase):

    def test_merge_all_options(self):
        options = {'-h': '200.200', '-p': 2020}
        self.assertEqual(options, merge_options(options))

    def test_merge_some_options(self):
        options = {'-p': 2020}
        expected = {'-h': '0.0.0.0', '-p': 2020}
        self.assertEqual(expected, merge_options(options))

    def test_merge_no_options(self):
        expected = {'-h': '0.0.0.0', '-p': 2222}
        self.assertEqual(expected, merge_options({}))

if __name__ == '__main__':
    unittest.main()
