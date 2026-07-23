import unittest
from protocol.serializer import Serializer
from protocol.parser import Parser

class TestProtocol(unittest.TestCase):
    def test_serializer(self):
        self.assertEqual(Serializer.simple_string("OK"), "+OK\r\n")
        self.assertEqual(Serializer.error("ERR unknown"), "-ERR ERR unknown\r\n")
        self.assertEqual(Serializer.integer(100), ":100\r\n")
        self.assertEqual(Serializer.bulk_string("hello"), "$5\r\nhello\r\n")
        self.assertEqual(Serializer.bulk_string(None), "$-1\r\n")
        self.assertEqual(Serializer.array(["foo", "bar"]), "*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n")

    def test_parser(self):
        parser = Parser()
        tokens = parser.parse("SET key value")
        self.assertEqual(tokens[0], "SET")
        self.assertEqual(tokens[1:], ["key", "value"])

        tokens = parser.parse("*2\r\n$3\r\nGET\r\n$3\r\nkey\r\n")
        self.assertEqual(tokens, ["GET", "key"])

if __name__ == "__main__":
    unittest.main()
