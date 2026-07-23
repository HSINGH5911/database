import unittest
from core.errors import (
    DatabaseError, CommandError, WrongTypeError,
    ProtocolError, StorageError, PageOverflowError
)

class TestErrors(unittest.TestCase):
    def test_database_error_resp(self):
        err = DatabaseError("Something went wrong")
        self.assertEqual(err.to_resp(), "-ERR Something went wrong\r\n")

    def test_wrong_type_error_resp(self):
        err = WrongTypeError()
        self.assertEqual(err.to_resp(), "-WRONGTYPE Operation against a key holding the wrong kind of value\r\n")

    def test_command_error(self):
        err = CommandError("Invalid argument count")
        self.assertEqual(err.to_resp(), "-ERR Invalid argument count\r\n")

if __name__ == "__main__":
    unittest.main()
