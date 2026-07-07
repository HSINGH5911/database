class Database:

    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value
    
    def get(self, key):
        return self.data.get(key)

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            return True

        return False
    
    def flush(self):
        self.data.clear()

    def exists(self, key):
        if key in self.data:
            return "(integer) 1"
        return "(integer) 0"
    
    def incr(self, key):
        value = self.data.get(key, 0)

        try:
            value = int(value)
        except ValueError:
            return "ERR - Value is not in range"
        
        value += 1

        self.data[key] = str(value)

        return value
    
    def decr(self, key):
        value = self.data.get(key, 0)

        try:
            value = int(value)
        except ValueError:
            return "ERR - Value is not in range"
        
        value -= 1

        self.data[key] = str(value)

        return value
    
    def append(self, key, message):
        if key not in self.data:
            return "ERR - value does not exist"
        
        value = self.data.get(key)

        value += message

        self.data[key] = value

        return "(integer) " + str(len(value))   