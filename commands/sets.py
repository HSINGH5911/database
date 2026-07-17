def format_set_response(res):
    if res is None:
        return "(nil)"
    if isinstance(res, str) and (res.startswith("WRONGTYPE") or res.startswith("ERR")):
        return res
    if isinstance(res, int):
        return f"(integer) {res}"
    if isinstance(res, (set, list)):
        if not res:
            return "(empty list or set)"
        # Check if list of integers (for SMISMEMBER)
        if isinstance(res, list) and all(isinstance(x, int) and not isinstance(x, bool) for x in res):
            lines = []
            for i, val in enumerate(res, 1):
                lines.append(f"{i}) (integer) {val}")
            return "\n".join(lines)
        lines = []
        for i, val in enumerate(sorted(list(res)), 1):
            lines.append(f"{i}) {val}")
        return "\n".join(lines)
    return res

def sadd_command(db, args):
    if len(args) < 2:
        return "ERR - wrong number of args"
    key = args[0]
    members = args[1:]

    res = db.sadd(key, *members)
    return format_set_response(res)

def srem_command(db, args):
    if len(args) < 2:
        return "ERR - wrong number of args"
    key = args[0]
    members = args[1:]

    res = db.srem(key, *members)
    return format_set_response(res)

def sismember_command(db, args):
    if len(args) != 2:
        return "ERR - wrong number of args"
    key = args[0]
    member = args[1]

    res = db.sismember(key, member)
    return format_set_response(res)

def smismember_command(db, args):
    if len(args) < 2:
        return "ERR - wrong number of args"
    key = args[0]
    members = args[1:]

    res = db.smismember(key, members)
    return format_set_response(res)

def scard_command(db, args):
    if len(args) != 1:
        return "ERR - wrong number of args"
    key = args[0]

    res = db.scard(key)
    return format_set_response(res)

def smembers_command(db, args):
    if len(args) != 1:
        return "ERR - wrong number of args"
    key = args[0]

    res = db.smembers(key)
    return format_set_response(res)

def spop_command(db, args):
    if len(args) < 1 or len(args) > 2:
        return "ERR - wrong number of args"
    key = args[0]

    count = None
    if len(args) == 2:
        try:
            count = int(args[1])
            if count < 0:
                return "ERR - value is not an integer or out of range"
        except ValueError:
            return "ERR - value is not an integer or out of range"

    res = db.spop(key, count)
    return format_set_response(res)

def srandommember_command(db, args):
    if len(args) < 1 or len(args) > 2:
        return "ERR - wrong number of args"
    key = args[0]

    count = None
    if len(args) == 2:
        try:
            count = int(args[1])
        except ValueError:
            return "ERR - value is not an integer or out of range"

    res = db.srandommember(key, count)
    return format_set_response(res)

def smove_command(db, args):
    if len(args) != 3:
        return "ERR - wrong number of args"
    origin = args[0]
    destination = args[1]
    item = args[2]

    res = db.smove(origin, destination, item)
    return format_set_response(res)

def sinter_command(db, args):
    if len(args) < 1:
        return "ERR - wrong number of args"
    keys = args[0:]

    res = db.sinter(keys)
    return format_set_response(res)

def sinterstore_command(db, args):
    if len(args) < 2:
        return "ERR - wrong number of args"
    dest = args[0]
    keys = args[1:]

    res = db.sinterstore(dest, keys)
    return format_set_response(res)

def sunion_command(db, args):
    if len(args) < 1:
        return "ERR - wrong number of args"
    keys = args[0:]

    res = db.sunion(keys)
    return format_set_response(res)

def sunionstore_command(db, args):
    if len(args) < 2:
        return "ERR - wrong number of args"
    dest = args[0]
    keys = args[1:]

    res = db.sunionstore(dest, keys)
    return format_set_response(res)

def sdiff_command(db, args):
    if len(args) < 1:
        return "ERR - wrong number of args"
    first_key = args[0]
    rest = args[1:]

    res = db.sdiff(first_key, rest)
    return format_set_response(res)

def sdiffstore_command(db, args):
    if len(args) < 2:
        return "ERR - wrong number of args"
    dest = args[0]
    keys = args[1:]

    res = db.sdiffstore(dest, keys)
    return format_set_response(res)