"""
Custom exception hierarchy for the database engine.
"""

class DatabaseError(Exception):
    """Base class for all database engine exceptions."""
    def __init__(self, message: str, code: str = "ERR"):
        super().__init__(message)
        self.message = message
        self.code = code

    def to_resp(self) -> str:
        """Serializes exception to RESP error string."""
        return f"-{self.code} {self.message}\r\n"


class CommandError(DatabaseError):
    """Raised when a command fails due to invalid syntax or execution error."""
    def __init__(self, message: str):
        super().__init__(message, code="ERR")


class WrongTypeError(DatabaseError):
    """Raised when an operation is attempted against a key holding the wrong data type."""
    def __init__(self, message: str = "WRONGTYPE Operation against a key holding the wrong kind of value"):
        super().__init__(message, code="WRONGTYPE")

    def to_resp(self) -> str:
        return f"-{self.message}\r\n"


class ProtocolError(DatabaseError):
    """Raised when RESP parsing or serialization fails."""
    def __init__(self, message: str):
        super().__init__(message, code="ERR Protocol error:")


class StorageError(DatabaseError):
    """Raised when page storage allocation or retrieval fails."""
    def __init__(self, message: str):
        super().__init__(message, code="ERR Storage error:")


class PageOverflowError(StorageError):
    """Raised when payload exceeds page memory limits."""
    def __init__(self, message: str = "Data size exceeds page capacity"):
        super().__init__(message)


class InvalidSlotError(StorageError):
    """Raised when attempting to read/write an invalid or deleted page slot."""
    def __init__(self, slot_id: int):
        super().__init__(f"Invalid or deleted slot ID: {slot_id}")


class PersistenceError(DatabaseError):
    """Raised when AOF or snapshot persistence fails."""
    def __init__(self, message: str):
        super().__init__(message, code="ERR Persistence error:")


class ConnectionError(DatabaseError):
    """Raised on socket/network connection issues."""
    def __init__(self, message: str):
        super().__init__(message, code="ERR Connection error:")
