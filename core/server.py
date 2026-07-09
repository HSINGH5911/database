from core.database import Database
from commands.registry import execute
from protocol.parser import Parser

class Server:
    def __init__(self):
        self.db = Database()
    
    def process(self, message):
        parts = Parser.parse(message)

        command = parts[0]
        args = parts[1:]

        return execute(command, self.db, args)