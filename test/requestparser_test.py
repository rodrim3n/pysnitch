import unittest
from client.objects import RequestParser

class TestRequestParser(unittest.TestCase):

    def test_parse_no_args_request(self):
        request = 'ls'
        request_parsed = RequestParser(request)
        self.assertEqual(request_parsed.command, 'ls')
        self.assertEqual(request_parsed.args, '')

    def test_parse_valid_request(self):
        request = 'ls->/home/pepe/'
        request_parsed = RequestParser(request)
        self.assertEqual(request_parsed.command, 'ls')
        self.assertEqual(request_parsed.args, '/home/pepe/')

    def test_parse_empty_request(self):
        request = ''
        request_parsed = RequestParser(request)
        self.assertEqual(request_parsed.command, '')
        self.assertEqual(request_parsed.args, '')

if __name__ == '__main__':
    unittest.main()
