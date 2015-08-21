import unittest
from client.objects import RequestParser

class TestRequestParser(unittest.TestCase):

    def test_parse_no_args_request(self):
        parsed_request = RequestParser('ls;')
        self.assertEqual(parsed_request.command, 'ls')
        self.assertEqual(parsed_request.args, '')
        self.assertTrue(parsed_request.is_valid)

    def test_parse_valid_request(self):
        parsed_request = RequestParser('ls;/home/pepe/')
        self.assertEqual(parsed_request.command, 'ls')
        self.assertEqual(parsed_request.args, '/home/pepe/')
        self.assertTrue(parsed_request.is_valid)

    def test_parse_lot_of_args(self):
        parsed_request = RequestParser('ls;/home/pepe/;/something')
        self.assertEqual(parsed_request.command, 'ls')
        self.assertEqual(parsed_request.args, '/home/pepe/')
        self.assertTrue(parsed_request.is_valid)

    def test_parse_empty_request(self):
        parsed_request = RequestParser('')
        self.assertFalse(parsed_request.is_valid)

    def test_parse_invalid_request(self):
        parsed_request = RequestParser(';')
        self.assertFalse(parsed_request.is_valid)

    def test_custom_delimiter(self):
        parsed_request = RequestParser('ls,/home/pepe/', ',')
        self.assertEqual(parsed_request.command, 'ls')
        self.assertEqual(parsed_request.args, '/home/pepe/')


if __name__ == '__main__':
    unittest.main()
