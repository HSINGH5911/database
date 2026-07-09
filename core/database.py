class Database:

    def __init__(self):
        self.data = {}

    # STRING COMMANDS 
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
    
    # HASH COMMANDS
    def hset(self, key, field, value):
        if key not in self.data:
            self.data[key] = {}
        self.data[key][field] = value

    def hget(self, key, field):
        if key not in self.data:
            return None
        return self.data[key].get(field)
    
    def hgetall(self, key):
        if key not in self.data:
            return None
        return self.data[key]
    
    def hdel(self, key, fields):
        if key not in self.data:
            return "(integer) 0"
        
        for field in fields:
            self.data[key].pop(field)
            
    
        return "(integer) " + str(len(fields))
    
    def hincrby(self, key, field, incr):
        try:
            int(incr)
        except ValueError:
            return "ERR - VALUE NOT IN RANGE"
        
        value = self.data.get(key, 0)
        
        value += incr

        self.data[key] = str(value)

        return value
    
    def hdecrby(self, key, field, decr):
        try:
            int(decr)
        except ValueError:
            return "ERR - VALUE NOT IN RANGE"
        
        value = self.data.get(key, 0)

        value -= decr

        self.data[key] = str(value)

        return value
    
    def hexists(self, key, field):
        if self.data[key].get(field):
            return "(integer 1)"
        return "(integer 0)"