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
    def lpush(self, key, *values):
        if key in self.data:
            if not isinstance(self.data[key], list):
                return "WRONGTYPE Operation against a key holding the wrong kind of value"
        else:
            self.data[key] = []
        
        for val in values:
            self.data[key].insert(0, val)
        return len(self.data[key])
    
    def rpush(self, key, *values):
        if key in self.data:
            if not isinstance(self.data[key], list):
                return "WRONGTYPE Operation against a key holding the wrong kind of value"
        else:
            self.data[key] = []
        
        for val in values:
            self.data[key].append(val)
        return len(self.data[key])

    def lpop(self, key, count=None):
        if key not in self.data:
            return None
        if not isinstance(self.data[key], list):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
        
        if not self.data[key]:
            return None
        
        if count is None:
            return self.data[key].pop(0)
        
        try:
            cnt = int(count)
        except ValueError:
            return "ERR - value is not an integer or out of range"
            
        if cnt < 0:
            return "ERR - value is not an integer or out of range"
            
        popped = []
        for _ in range(min(cnt, len(self.data[key]))):
            popped.append(self.data[key].pop(0))
        return popped
    
    def rpop(self, key, count=None):
        if key not in self.data:
            return None
        if not isinstance(self.data[key], list):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
        
        if not self.data[key]:
            return None
        
        if count is None:
            return self.data[key].pop()
        
        try:
            cnt = int(count)
        except ValueError:
            return "ERR - value is not an integer or out of range"
            
        if cnt < 0:
            return "ERR - value is not an integer or out of range"
            
        popped = []
        for _ in range(min(cnt, len(self.data[key]))):
            popped.append(self.data[key].pop())
        return popped
    
    def lrem(self, key, count, value):
        if key not in self.data:
            return 0
        if not isinstance(self.data[key], list):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
        
        try:
            cnt = int(count)
        except ValueError:
            return "ERR - value is not an integer or out of range"
            
        lst = self.data[key]
        removed = 0
        
        if cnt > 0:
            i = 0
            while i < len(lst) and removed < cnt:
                if lst[i] == value:
                    lst.pop(i)
                    removed += 1
                else:
                    i += 1
        elif cnt < 0:
            limit = abs(cnt)
            i = len(lst) - 1
            while i >= 0 and removed < limit:
                if lst[i] == value:
                    lst.pop(i)
                    removed += 1
                i -= 1
        else:
            i = 0
            while i < len(lst):
                if lst[i] == value:
                    lst.pop(i)
                    removed += 1
                else:
                    i += 1
        
        return removed
    
    def ltrim(self, key, start, stop):
        if key not in self.data:
            return "OK"
        if not isinstance(self.data[key], list):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
        
        try:
            start_idx = int(start)
            stop_idx = int(stop)
        except ValueError:
            return "ERR - value is not an integer or out of range"
            
        lst = self.data[key]
        n = len(lst)
        
        if start_idx < 0:
            start_idx = max(0, n + start_idx)
        if stop_idx < 0:
            stop_idx = n + stop_idx
            
        if start_idx >= n or start_idx > stop_idx:
            self.data[key] = []
        else:
            stop_idx = min(stop_idx, n - 1)
            self.data[key] = lst[start_idx:stop_idx + 1]
            
        return "OK"

    def lrange(self, key, start, stop):
        if key not in self.data:
            return None
        if not isinstance(self.data[key], list):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
            
        try:
            start_idx = int(start)
            stop_idx = int(stop)
        except ValueError:
            return "ERR - value is not an integer or out of range"
            
        lst = self.data[key]
        n = len(lst)
        
        if start_idx < 0:
            start_idx = max(0, n + start_idx)
        if stop_idx < 0:
            stop_idx = n + stop_idx
            
        if start_idx >= n or start_idx > stop_idx:
            return []
            
        stop_idx = min(stop_idx, n - 1)
        return lst[start_idx:stop_idx + 1]
    
    def lindex(self, key, index):
        if key not in self.data:
            return None
        if not isinstance(self.data[key], list):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
            
        try:
            idx = int(index)
        except ValueError:
            return "ERR - value is not an integer or out of range"
            
        lst = self.data[key]
        n = len(lst)
        
        if idx < 0:
            idx = n + idx
            
        if idx < 0 or idx >= n:
            return None
            
        return lst[idx]
    
    def llen(self, key):
        if key not in self.data:
            return 0
        if not isinstance(self.data[key], list):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
        
        return len(self.data[key])
    
    def rpoplpush(self, source, destination):
        if source not in self.data:
            return None
        if not isinstance(self.data[source], list):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
            
        if destination in self.data:
            if not isinstance(self.data[destination], list):
                return "WRONGTYPE Operation against a key holding the wrong kind of value"
        else:
            self.data[destination] = []
            
        if not self.data[source]:
            return None
            
        val = self.data[source].pop()
        self.data[destination].insert(0, val)
        return val
    
    def lmove(self, source, destination, wherefrom, whereto):
        if source not in self.data:
            return None
        if not isinstance(self.data[source], list):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
            
        if destination in self.data:
            if not isinstance(self.data[destination], list):
                return "WRONGTYPE Operation against a key holding the wrong kind of value"
        else:
            self.data[destination] = []
            
        wf = wherefrom.upper()
        wt = whereto.upper()
        
        if wf not in ("LEFT", "RIGHT") or wt not in ("LEFT", "RIGHT"):
            return "ERR - syntax error"
            
        if not self.data[source]:
            return None
            
        if wf == "LEFT":
            val = self.data[source].pop(0)
        else:
            val = self.data[source].pop()
            
        if wt == "LEFT":
            self.data[destination].insert(0, val)
        else:
            self.data[destination].append(val)
            
        return val

        