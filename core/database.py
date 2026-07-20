import random
import fnmatch
import time

class SortedSet:
    def __init__(self):
        self.mapping = {}

    def add(self, member, score):
        is_new = member not in self.mapping
        self.mapping[member] = float(score)
        return is_new

    def remove(self, member):
        if member in self.mapping:
            del self.mapping[member]
            return True
        return False

    def get_score(self, member):
        return self.mapping.get(member)

    def __len__(self):
        return len(self.mapping)

    def __bool__(self):
        return bool(self.mapping)

    def get_sorted(self, reverse=False):
        if not reverse:
            return sorted(self.mapping.items(), key=lambda item: (item[1], item[0]))
        else:
            return sorted(self.mapping.items(), key=lambda item: (item[1], item[0]), reverse=True)


def parse_score_bound(val_str):
    val_str = str(val_str).strip()
    exclusive = False
    if val_str.startswith("("):
        exclusive = True
        val_str = val_str[1:]
    
    val_lower = val_str.lower()
    if val_lower in ("-inf", "-infinity"):
        val = float("-inf")
    elif val_lower in ("+inf", "+infinity", "inf", "infinity"):
        val = float("inf")
    else:
        val = float(val_str)
        
    return val, exclusive


def score_in_range(s, min_val, min_ex, max_val, max_ex):
    if min_ex:
        if s <= min_val:
            return False
    else:
        if s < min_val:
            return False
            
    if max_ex:
        if s >= max_val:
            return False
    else:
        if s > max_val:
            return False
            
    return True


class Database:

    def __init__(self):
        self.data = {}
        self.channels = {}
        self.start_time = time.time()

    """
    STRING COMMANDS
    """
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
    
    """
    HASH COMMANDS
    """
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
    
    """
    LIST COMMANDS
    """
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

    """
    SET COMMANDS
    """
    def sadd(self, key, *members):
        if key in self.data:
            if not isinstance(self.data[key], set):
                return "WRONGTYPE Operation against a key holding the wrong kind of value"
        else:
            self.data[key] = set()
        
        added = 0
        for member in members:
            if member not in self.data[key]:
                self.data[key].add(member)
                added += 1

        return added
    
    def srem(self, key, *members):
        if key not in self.data:
            return 0
        if not isinstance(self.data[key], set):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
        
        removed = 0
        for member in members:
            if member in self.data[key]:
                self.data[key].remove(member)
                removed += 1

        if not self.data[key]:
            del self.data[key]

        return removed

    def sismember(self, key, member):
        if key not in self.data:
            return 0
        if not isinstance(self.data[key], set):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"

        return 1 if member in self.data[key] else 0
    
    def smismember(self, key, members):
        if key in self.data and not isinstance(self.data[key], set):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
        
        results = []
        for member in members:
            results.append(self.sismember(key, member))
        return results

    def scard(self, key):
        if key not in self.data:
            return 0
        if not isinstance(self.data[key], set):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
        return len(self.data[key])
    
    def smembers(self, key):
        if key not in self.data:
            return set()
        if not isinstance(self.data[key], set):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
        return self.data[key]
    
    def spop(self, key, count=None):
        if key not in self.data:
            return None
        if not isinstance(self.data[key], set):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
        
        if not self.data[key]:
            return None
            
        if count is None:
            elem = random.choice(list(self.data[key]))
            self.data[key].remove(elem)
            if not self.data[key]:
                del self.data[key]
            return elem
            
        popped = []
        limit = min(count, len(self.data[key]))
        for _ in range(limit):
            elem = random.choice(list(self.data[key]))
            self.data[key].remove(elem)
            popped.append(elem)
            
        if not self.data[key]:
            del self.data[key]
            
        return popped

    def srandommember(self, key, count=None):
        if key not in self.data:
            return None
        if not isinstance(self.data[key], set):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
        
        if not self.data[key]:
            return None
            
        elements = list(self.data[key])
        
        if count is None:
            return random.choice(elements)
            
        if count >= 0:
            limit = min(count, len(elements))
            return random.sample(elements, limit)
        else:
            limit = abs(count)
            return [random.choice(elements) for _ in range(limit)]
    
    def smove(self, origin, destination, item):
        if origin not in self.data:
            return 0
        if not isinstance(self.data[origin], set):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
        if destination in self.data and not isinstance(self.data[destination], set):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
            
        if item not in self.data[origin]:
            return 0
            
        self.data[origin].remove(item)
        if not self.data[origin]:
            del self.data[origin]
            
        if destination not in self.data:
            self.data[destination] = set()
        self.data[destination].add(item)
        
        return 1

    def sinter(self, keys):
        if not keys:
            return []
            
        for key in keys:
            if key in self.data and not isinstance(self.data[key], set):
                return "WRONGTYPE Operation against a key holding the wrong kind of value"
                
        for key in keys:
            if key not in self.data:
                return []
                
        result = set(self.data[keys[0]])
        for key in keys[1:]:
            result = result.intersection(self.data[key])
            
        return list(result)

    def sinterstore(self, dest, keys):
        if dest in self.data and not isinstance(self.data[dest], set):
            del self.data[dest]
            
        res = self.sinter(keys)
        if isinstance(res, str) and res.startswith("WRONGTYPE"):
            return res
            
        if not res:
            if dest in self.data:
                del self.data[dest]
            return 0
            
        self.data[dest] = set(res)
        return len(self.data[dest])
    
    def sunion(self, keys):
        if not keys:
            return []
            
        for key in keys:
            if key in self.data and not isinstance(self.data[key], set):
                return "WRONGTYPE Operation against a key holding the wrong kind of value"
                
        result = set()
        for key in keys:
            if key in self.data:
                result = result.union(self.data[key])
                
        return list(result)
    
    def sunionstore(self, dest, keys):
        if dest in self.data:
            del self.data[dest]
            
        res = self.sunion(keys)
        if isinstance(res, str) and res.startswith("WRONGTYPE"):
            return res
            
        if not res:
            return 0
            
        self.data[dest] = set(res)
        return len(self.data[dest])
    
    def sdiff(self, first, rest):
        if first in self.data and not isinstance(self.data[first], set):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
        for key in rest:
            if key in self.data and not isinstance(self.data[key], set):
                return "WRONGTYPE Operation against a key holding the wrong kind of value"
                
        if first not in self.data:
            return []
            
        result = set(self.data[first])
        for key in rest:
            if key in self.data:
                result = result.difference(self.data[key])
                
        return list(result)
    
    def sdiffstore(self, dest, keys):
        if not keys:
            return 0
            
        if dest in self.data:
            del self.data[dest]
            
        res = self.sdiff(keys[0], keys[1:])
        if isinstance(res, str) and res.startswith("WRONGTYPE"):
            return res
            
        if not res:
            return 0
            
        self.data[dest] = set(res)
        return len(self.data[dest])

    """
    SORTED SET COMMANDS
    """
    def zadd(self, key, pairs):
        if key in self.data:
            if not isinstance(self.data[key], SortedSet):
                return "WRONGTYPE Operation against a key holding the wrong kind of value"
        else:
            self.data[key] = SortedSet()

        added = 0
        for score_str, member in pairs:
            try:
                score = float(score_str)
            except ValueError:
                return "ERR - value is not a valid float"
            if self.data[key].add(member, score):
                added += 1

        return added

    def zrem(self, key, *members):
        if key not in self.data:
            return 0
        if not isinstance(self.data[key], SortedSet):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"

        removed = 0
        for member in members:
            if self.data[key].remove(member):
                removed += 1

        if not self.data[key]:
            del self.data[key]

        return removed

    def zscore(self, key, member):
        if key not in self.data:
            return None
        if not isinstance(self.data[key], SortedSet):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"

        score = self.data[key].get_score(member)
        if score is None:
            return None
        return str(int(score)) if score.is_integer() else str(score)

    def zincrby(self, key, increment, member):
        try:
            incr_val = float(increment)
        except ValueError:
            return "ERR - value is not a valid float"

        if key in self.data:
            if not isinstance(self.data[key], SortedSet):
                return "WRONGTYPE Operation against a key holding the wrong kind of value"
        else:
            self.data[key] = SortedSet()

        curr_score = self.data[key].get_score(member)
        if curr_score is None:
            curr_score = 0.0

        new_score = curr_score + incr_val
        self.data[key].add(member, new_score)

        return str(int(new_score)) if new_score.is_integer() else str(new_score)

    def zcard(self, key):
        if key not in self.data:
            return 0
        if not isinstance(self.data[key], SortedSet):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"
        return len(self.data[key])

    def zcount(self, key, min_str, max_str):
        try:
            min_val, min_ex = parse_score_bound(min_str)
            max_val, max_ex = parse_score_bound(max_str)
        except ValueError:
            return "ERR - min or max is not a float"

        if key not in self.data:
            return 0
        if not isinstance(self.data[key], SortedSet):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"

        count = 0
        for member, score in self.data[key].mapping.items():
            if score_in_range(score, min_val, min_ex, max_val, max_ex):
                count += 1
        return count

    def zrange(self, key, start, stop, withscores=False, reverse=False):
        try:
            start_idx = int(start)
            stop_idx = int(stop)
        except ValueError:
            return "ERR - value is not an integer or out of range"

        if key not in self.data:
            return []
        if not isinstance(self.data[key], SortedSet):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"

        items = self.data[key].get_sorted(reverse=reverse)
        n = len(items)
        if start_idx < 0:
            start_idx = max(0, n + start_idx)
        if stop_idx < 0:
            stop_idx = n + stop_idx

        if start_idx >= n or start_idx > stop_idx:
            return []

        stop_idx = min(stop_idx, n - 1)
        sub = items[start_idx:stop_idx + 1]

        result = []
        for m, s in sub:
            result.append(m)
            if withscores:
                score_str = str(int(s)) if s.is_integer() else str(s)
                result.append(score_str)

        return result

    def zrevrange(self, key, start, stop, withscores=False):
        return self.zrange(key, start, stop, withscores=withscores, reverse=True)

    def zrangebyscore(self, key, min_str, max_str, withscores=False, offset=None, count=None):
        try:
            min_val, min_ex = parse_score_bound(min_str)
            max_val, max_ex = parse_score_bound(max_str)
        except ValueError:
            return "ERR - min or max is not a float"

        if key not in self.data:
            return []
        if not isinstance(self.data[key], SortedSet):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"

        items = self.data[key].get_sorted(reverse=False)
        filtered = [
            (m, s) for m, s in items
            if score_in_range(s, min_val, min_ex, max_val, max_ex)
        ]

        if offset is not None and count is not None:
            filtered = filtered[offset:offset + count]

        result = []
        for m, s in filtered:
            result.append(m)
            if withscores:
                score_str = str(int(s)) if s.is_integer() else str(s)
                result.append(score_str)

        return result

    def zrank(self, key, member, reverse=False):
        if key not in self.data:
            return None
        if not isinstance(self.data[key], SortedSet):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"

        items = self.data[key].get_sorted(reverse=reverse)
        for rank, (m, s) in enumerate(items):
            if m == member:
                return rank
        return None

    def zrevrank(self, key, member):
        return self.zrank(key, member, reverse=True)

    def zpopmin(self, key, count=1):
        if key not in self.data:
            return []
        if not isinstance(self.data[key], SortedSet):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"

        if not self.data[key]:
            return []

        items = self.data[key].get_sorted(reverse=False)
        to_pop = items[:count]

        result = []
        for m, s in to_pop:
            self.data[key].remove(m)
            score_str = str(int(s)) if s.is_integer() else str(s)
            result.extend([m, score_str])

        if not self.data[key]:
            del self.data[key]

        return result

    def zpopmax(self, key, count=1):
        if key not in self.data:
            return []
        if not isinstance(self.data[key], SortedSet):
            return "WRONGTYPE Operation against a key holding the wrong kind of value"

        if not self.data[key]:
            return []

        items = self.data[key].get_sorted(reverse=True)
        to_pop = items[:count]

        result = []
        for m, s in to_pop:
            self.data[key].remove(m)
            score_str = str(int(s)) if s.is_integer() else str(s)
            result.extend([m, score_str])

        if not self.data[key]:
            del self.data[key]

        return result
    
    """
    PUBSUB COMMANDS
    """
    def subscribe(self, client_socket, *channel_names):
        results = []
        
        for channel in channel_names:
            if channel not in channel_names:
                self.channels[channel] = set()
        
            self.channels[channel].add(client_socket)
            sub_count = len([ch for ch, clients in self.channels.items() if client_socket in clients])
            results.append(["subscribe", channel, sub_count])
        
        return results
    
    def unsubscribe(self, client_socket, *channel_names):
        if not channel_names:
            channel_names = [ch for ch, clients in self.channels.items() if client_socket in clients]
        
        results = []                                                                                                                                                                           
        
        for channel in channel_names:                                                                                                                                                          
            if channel in self.channels and client_socket in self.channels[channel]:                                                                                                           
                self.channels[channel].remove(client_socket)                                                                                                                                   
                if not self.channels[channel]:                                                                                                                                                 
                    del self.channels[channel]                                                                                                                                                 
            
            sub_count = len([ch for ch, clients in self.channels.items() if client_socket in clients])                                                                                         
            results.append(["unsubscribe", channel, sub_count])                                                                                                                                
        
        return results  
    
    def publish(self, channel, message):                                                                                                                                                       
        if channel not in self.channels:                                                                                                                                                       
            return 0                                                                                                                                                                           
                                                                                                                                                                                                
        subscribers = list(self.channels[channel])                                                                                                                                             
        received_count = 0                                                                                                                                                                     
                                                                                                                                                                                                
        # Format pubsub message payload                                                                                                                                                        
        payload = f"1) \"message\"\n2) \"{channel}\"\n3) \"{message}\"\n\n".encode()                                                                                                           
                                                                                                                                                                                                
        for client_socket in subscribers:                                                                                                                                                      
            try:                                                                                                                                                                               
                client_socket.send(payload)                                                                                                                                                    
                received_count += 1                                                                                                                                                            
            except Exception:                                                                                                                                                                  
                # Remove stale/closed socket connections                                                                                                                                       
                self.channels[channel].discard(client_socket)                                                                                                                                  
                                                                                                                                                                                                
        return received_count

    """
    ADMINISTRATIVE COMMANDS
    """
    def dbsize(self):
        return len(self.data)

    def keys(self, pattern="*"):
        matching = []
        for key in self.data.keys():
            if fnmatch.fnmatch(key, pattern):
                matching.append(key)
        return matching

    def type(self, key):
        if key not in self.data:
            return "none"
        val = self.data[key]
        if isinstance(val, SortedSet):
            return "zset"
        elif isinstance(val, set):
            return "set"
        elif isinstance(val, list):
            return "list"
        elif isinstance(val, dict):
            return "hash"
        elif isinstance(val, str):
            return "string"
        return "unknown"

    def rename(self, key, newkey):
        if key not in self.data:
            return False
        self.data[newkey] = self.data.pop(key)
        return True

    def renamenx(self, key, newkey):
        if key not in self.data:
            return "ERR no such key"
        if newkey in self.data:
            return 0
        self.data[newkey] = self.data.pop(key)
        return 1

    def randomkey(self):
        if not self.data:
            return None
        return random.choice(list(self.data.keys()))

    def info(self):
        uptime_sec = int(time.time() - self.start_time)
        info_lines = [
            "# Server",
            "redis_version:7.0.0-like",
            f"uptime_in_seconds:{uptime_sec}",
            "# Keyspace",
            f"db0:keys={len(self.data)},expires=0,avg_ttl=0"
        ]
        return "\n".join(info_lines)

    def time(self):
        now = time.time()
        seconds = int(now)
        microseconds = int((now - seconds) * 1000000)
        return [str(seconds), str(microseconds)]     