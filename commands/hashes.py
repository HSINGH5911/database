def hset_command(db, args):
    if len(args) != 3:
        return "ERR - wrong number of args"
    key = args[0]
    field = args[1]
    value = args[2]

    return db.hset(key, field, value)

def hget_command(db, args):
    if len(args) != 2:
        return "ERR - wrong number of args"
    key = args[0]
    field = args[1]

    res = db.hget(key, field)
    if res is None:
        return "(nil)"
    return res

def hgetall_command(db, args):
    if len(args) != 1:
        return "ERR - wrong number of args"
    key = args[0]

    res = db.hgetall(key)
    if res is None:
        return "(empty list or set)"
    if isinstance(res, str) and res.startswith("WRONGTYPE"):
        return res
    if not isinstance(res, dict):
        return "ERR - server error"
    
    if not res:
        return "(empty list or set)"
    
    lines = []
    idx = 1
    for k, v in res.items():
        lines.append(f"{idx}) {k}")
        lines.append(f"{idx+1}) {v}")
        idx += 2
    return "\n".join(lines)

def hdel_command(db, args):
    if len(args) < 2:
        return "ERR - wrong number of args"
    key = args[0]
    fields = args[1:]

    return db.hdel(key, fields)

def hincrby_command(db, args):
    if len(args) != 3:
        return "ERR - wrong number of args"
    key = args[0]
    field = args[1]
    incr = args[2]

    return db.hincrby(key, field, incr)

def hdecrby_command(db, args):
    if len(args) != 3:
        return "ERR - wrong number of args"
    key = args[0]
    field = args[1]
    decr = args[2]

    return db.hdecrby(key, field, decr)

def hexists_command(db, args):
    if len(args) != 2:
        return "ERR - wrong number of args"
    key = args[0]
    field = args[1]

    return db.hexists(key, field)
