from protocol.parser import Parser
from protocol.serializer import Serializer

class Protocol:

    def __init__(self):
        self.parser = Parser()
        self.serializer = Serializer()