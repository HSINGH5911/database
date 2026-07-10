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
    
    # LIST COMMANDS
    def lpush(self, key, value):
        if key not in self.data:
            self.data[key] = []

        self.data[key].insert(0, value)

        return len(self.data[key])
    
    def rpush(self, key, value):
        if key not in self.data:
            self.data[key] = []

        self.data[key].append(value)

        return len(self.data[key])

    def lpop(self, key, amount):
        if len(self.data) < amount:
            return "ERR - Not Enough Values In Data To Pop"
        
        removed = []

        for i in range(amount):
            removed.append(self.data[key].pop(0))

        return removed
    
    def rpop(self, key, amount):
        if len(self.data) < amount:
            return "ERR - Not Enough Values In Data To Pop"
        
        removed = []

        for i in range(amount):
            removed.append(self.data[key].pop())
        
        return removed
    
    def lrem(self, key, count, value):
        removed = 0
        
        if count > 0:
            for i in range(count):
                if self.data[key].get(i) == value:
                    removed += 1
                    self.data[key].pop(i)
                    i -= 1
            
            return removed
        
        if count < 0:
            for i in range((len(self.data[key]), count, -1)):
                if self.data[key].get(i) == value:
                    removed += 1
                    self.data[key].pop(i)
                    i -= 1

            return removed

        for i in range(len(self.data[key].items())):
            if self.data[key].get(i) == value:
                removed += 1
                self.data[key].pop(i)
                i -= 1
        
        return removed
    
    def lrim(self, key, start, stop):
        if key not in self.data:
            return "ERR - Key Does Not Exist"
        
        new_data = {}

        for i in range(start, stop):
            new_data[i] = self.data[key].get(i)
        
        self.data[key] = new_data

    def lrange(self, key, start, stop):
        if key not in self.data:
            return []

        show = self.data[key]

        return show[start:stop + 1]
    
    def lindex(self, key, index):
        if key not in self.data:
            return -1
        
        return self.data[key].get(index)
    
    def llen(self, key):
        if key not in self.data:
            return -1
        
        return len(self.data[key])
    
    def rpoplpush(self, source, destination):
        if source not in self.data:
            return "nil"
        if destination not in self.data:
            return "nil"
        
        move = self.rpop(source, 1)
        self.lpush(destination, move)

        return move
    
    def lmove(self, source, destination, lr1, lr2):
        if source not in self.data:
            return "nil"
        if destination not in self.data:
            return "nil"
        if not lr1 == "RIGHT" or lr1 == "LEFT":
            return "ERR - Specify 'Right' or 'Left'"
        if not lr2 == "RIGHT" or lr2 == "LEFT":
            return "ERR - Specify 'Right' or 'Left'"
        
        move = None

        if lr1 == "RIGHT":
            move = self.rpop(source, 1)
        if lr1 == "LEFT":
            move = self.lpop(source, 1)

        if lr2 == "RIGHT":
            self.rpush(destination, move)
        if lr2 == "LEFT":
            self.lpush(destination, move)

        return move

        