def lpush_command(db, args):
    if len(args) < 2:
        return "ERR - wrong number of args"
    key = args[0]
    values = args[1:]

    return db.lpush(key, *values)

def rpush_command(db, args):
    if len(args) < 2:
        return "ERR - wrong number of args"
    key = args[0]
    values = args[1:]

    return db.rpush(key, *values)

def lpop_command(db, args):
    if len(args) < 1 or len(args) > 2:
        return "ERR - wrong number of args"
    key = args[0]
    count = args[1] if len(args) == 2 else None

    res = db.lpop(key, count)
    if res is None:
        return "(nil)"
    if isinstance(res, list):
        if not res:
            return "(nil)"
        lines = []
        for i, val in enumerate(res, 1):
            lines.append(f"{i}) {val}")
        return "\n".join(lines)
    return res

def rpop_command(db, args):
    if len(args) < 1 or len(args) > 2:
        return "ERR - wrong number of args"
    key = args[0]
    count = args[1] if len(args) == 2 else None

    res = db.rpop(key, count)
    if res is None:
        return "(nil)"
    if isinstance(res, list):
        if not res:
            return "(nil)"
        lines = []
        for i, val in enumerate(res, 1):
            lines.append(f"{i}) {val}")
        return "\n".join(lines)
    return res

def lrem_command(db, args):
    if len(args) != 3:
        return "ERR - wrong number of args"
    key = args[0]
    count = args[1]
    value = args[2]

    res = db.lrem(key, count, value)
    if isinstance(res, int):
        return f"(integer) {res}"
    return res

def ltrim_command(db, args):
    if len(args) != 3:
        return "ERR - wrong number of args"
    key = args[0]
    start = args[1]
    stop = args[2]

    return db.ltrim(key, start, stop)

def lrange_command(db, args):
    if len(args) != 3:
        return "ERR - wrong number of args"
    key = args[0]
    start = args[1]
    stop = args[2]

    res = db.lrange(key, start, stop)
    if res is None:
        return "(empty list or set)"
    if isinstance(res, str) and (res.startswith("WRONGTYPE") or res.startswith("ERR")):
        return res
    if not res:
        return "(empty list or set)"
    
    lines = []
    for i, val in enumerate(res, 1):
        lines.append(f"{i}) {val}")
    return "\n".join(lines)

def lindex_command(db, args):
    if len(args) != 2:
        return "ERR - wrong number of args"
    key = args[0]
    index = args[1]

    res = db.lindex(key, index)
    if res is None:
        return "(nil)"
    return res

def llen_command(db, args):
    if len(args) != 1:
        return "ERR - wrong number of args"
    key = args[0]

    res = db.llen(key)
    if isinstance(res, int):
        return f"(integer) {res}"
    return res

def rpoplpush_command(db, args):
    if len(args) != 2:
        return "ERR - wrong number of args"
    source = args[0]
    destination = args[1]

    res = db.rpoplpush(source, destination)
    if res is None:
        return "(nil)"
    return res

def lmove_command(db, args):
    if len(args) != 4:
        return "ERR - wrong number of args"
    source = args[0]
    destination = args[1]
    left_right_1 = args[2]
    left_right_2 = args[3]

    res = db.lmove(source, destination, left_right_1, left_right_2)
    if res is None:
        return "(nil)"
    return res

lrim_command = ltrim_command
