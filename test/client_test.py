import unittest
from client.objects import Client

class TestClient(unittest.TestCase):

    def test_fetch_valid_command(self):
        client = Client(123,123)
        command = client.fetch_command('ls')
        self.assertTrue(callable(command.run))

    def test_fetch_invalid_command(self):
        client = Client(123,123)
        self.assertRaises(AttributeError, client.fetch_command, 'naosidnfoai')



if __name__ == '__main__':
    unittest.main()
