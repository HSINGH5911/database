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
        if key in self.data:
            if not isinstance(self.data[key], dict):
                return "WRONGTYPE Operation against a key holding the wrong kind of value"
        else:
            self.data[key] = {}
        
        is_new = field not in self.data[key]
        self.data[key][field] = value
        return f"(integer) {1 if is_new else 0}"

    def hget(self, key, field):
        if key not in self.data:
            return None
        if not isinstance(self.data[key], dict):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
        return self.data[key].get(field)
    
    def hgetall(self, key):
        if key not in self.data:
            return None
        if not isinstance(self.data[key], dict):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
        return self.data[key]
    
    def hdel(self, key, fields):
        if key not in self.data:
            return "(integer) 0"
        if not isinstance(self.data[key], dict):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
        
        deleted_count = 0
        for field in fields:
            if field in self.data[key]:
                self.data[key].pop(field)
                deleted_count += 1
    
        return f"(integer) {deleted_count}"
    
    def hincrby(self, key, field, incr):
        try:
            incr_val = int(incr)
        except ValueError:
            return "ERR - value is not an integer or out of range"
        
        if key in self.data:
            if not isinstance(self.data[key], dict):
                return "WRONGTYPE Operation against a key holding the wrong kind of value"
        else:
            self.data[key] = {}
        
        current_val_str = self.data[key].get(field, "0")
        try:
            current_val = int(current_val_str)
        except ValueError:
            return "ERR - hash value is not an integer"
        
        new_val = current_val + incr_val
        self.data[key][field] = str(new_val)
        return new_val
    
    def hdecrby(self, key, field, decr):
        try:
            decr_val = int(decr)
        except ValueError:
            return "ERR - value is not an integer or out of range"
        
        if key in self.data:
            if not isinstance(self.data[key], dict):
                return "WRONGTYPE Operation against a key holding the wrong kind of value"
        else:
            self.data[key] = {}
        
        current_val_str = self.data[key].get(field, "0")
        try:
            current_val = int(current_val_str)
        except ValueError:
            return "ERR - hash value is not an integer"
        
        new_val = current_val - decr_val
        self.data[key][field] = str(new_val)
        return new_val
    
    def hexists(self, key, field):
        if key not in self.data:
            return "(integer) 0"
        if not isinstance(self.data[key], dict):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
        
        if field in self.data[key]:
            return "(integer) 1"
        return "(integer) 0"
    