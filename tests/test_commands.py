import unittest
from core.database import Database
from commands.registry import execute

class TestCommands(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def test_string_commands(self):
        res = execute("SET", self.db, ["key1", "value1"])
        self.assertEqual(res, "OK")

        res = execute("GET", self.db, ["key1"])
        self.assertEqual(res, "value1")

        res = execute("EXISTS", self.db, ["key1"])
        self.assertIn("1", str(res))

        res = execute("DEL", self.db, ["key1"])
        self.assertEqual(res, 1)

    def test_ping_command(self):
        res = execute("PING", self.db, [])
        self.assertEqual(res, "PONG")

    def test_unknown_command(self):
        with self.assertRaises(Exception):
            execute("UNKNOWN_CMD", self.db, [])

if __name__ == "__main__":
    unittest.main()
