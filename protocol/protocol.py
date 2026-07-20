from protocol.parser import Parser
from protocol.serializer import Serializer

class Protocol:

    def __init__(self):
        self.parser = Parser()
        self.serializer = Serializer()

    def parse_request(self, raw_data):
        tokens = self.parser.parse(raw_data)
        if not tokens:
            return None, []
        command = tokens[0]
        args = tokens[1:]
        return command, args

    def serialize_response(self, result):
        return self.serializer.serialize(result)