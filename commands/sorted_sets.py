def format_zset_response(res):
    if res is None:
        return "(nil)"
    if isinstance(res, str) and (res.startswith("WRONGTYPE") or res.startswith("ERR")):
        return res
    if isinstance(res, int):
        return f"(integer) {res}"
    if isinstance(res, list):
        if not res:
            return "(empty list or set)"
        lines = []
        for i, val in enumerate(res, 1):
            lines.append(f"{i}) {val}")
        return "\n".join(lines)
    return str(res)

def zadd_command(db, args):
    if len(args) < 3 or (len(args) - 1) % 2 != 0:
        return "ERR - wrong number of args"
    key = args[0]
    pairs = []
    for i in range(1, len(args), 2):
        pairs.append((args[i], args[i+1]))

    res = db.zadd(key, pairs)
    return format_zset_response(res)

def zrem_command(db, args):
    if len(args) < 2:
        return "ERR - wrong number of args"
    key = args[0]
    members = args[1:]

    res = db.zrem(key, *members)
    return format_zset_response(res)

def zscore_command(db, args):
    if len(args) != 2:
        return "ERR - wrong number of args"
    key = args[0]
    member = args[1]

    res = db.zscore(key, member)
    return format_zset_response(res)

def zincrby_command(db, args):
    if len(args) != 3:
        return "ERR - wrong number of args"
    key = args[0]
    increment = args[1]
    member = args[2]

    res = db.zincrby(key, increment, member)
    return format_zset_response(res)

def zcard_command(db, args):
    if len(args) != 1:
        return "ERR - wrong number of args"
    key = args[0]

    res = db.zcard(key)
    return format_zset_response(res)

def zcount_command(db, args):
    if len(args) != 3:
        return "ERR - wrong number of args"
    key = args[0]
    min_val = args[1]
    max_val = args[2]

    res = db.zcount(key, min_val, max_val)
    return format_zset_response(res)

def zrange_command(db, args):
    if len(args) < 3 or len(args) > 4:
        return "ERR - wrong number of args"
    key = args[0]
    start = args[1]
    stop = args[2]
    withscores = False
    if len(args) == 4:
        if args[3].upper() == "WITHSCORES":
            withscores = True
        else:
            return "ERR - syntax error"

    res = db.zrange(key, start, stop, withscores=withscores)
    return format_zset_response(res)

def zrevrange_command(db, args):
    if len(args) < 3 or len(args) > 4:
        return "ERR - wrong number of args"
    key = args[0]
    start = args[1]
    stop = args[2]
    withscores = False
    if len(args) == 4:
        if args[3].upper() == "WITHSCORES":
            withscores = True
        else:
            return "ERR - syntax error"

    res = db.zrevrange(key, start, stop, withscores=withscores)
    return format_zset_response(res)

def zrangebyscore_command(db, args):
    if len(args) < 3:
        return "ERR - wrong number of args"
    key = args[0]
    min_val = args[1]
    max_val = args[2]
    withscores = False
    offset = None
    count = None

    idx = 3
    while idx < len(args):
        arg_upper = args[idx].upper()
        if arg_upper == "WITHSCORES":
            withscores = True
            idx += 1
        elif arg_upper == "LIMIT":
            if idx + 2 >= len(args):
                return "ERR - syntax error"
            try:
                offset = int(args[idx + 1])
                count = int(args[idx + 2])
            except ValueError:
                return "ERR - value is not an integer or out of range"
            idx += 3
        else:
            return "ERR - syntax error"

    res = db.zrangebyscore(key, min_val, max_val, withscores=withscores, offset=offset, count=count)
    return format_zset_response(res)

def zrank_command(db, args):
    if len(args) != 2:
        return "ERR - wrong number of args"
    key = args[0]
    member = args[1]

    res = db.zrank(key, member)
    return format_zset_response(res)

def zrevrank_command(db, args):
    if len(args) != 2:
        return "ERR - wrong number of args"
    key = args[0]
    member = args[1]

    res = db.zrevrank(key, member)
    return format_zset_response(res)

def zpopmin_command(db, args):
    if len(args) < 1 or len(args) > 2:
        return "ERR - wrong number of args"
    key = args[0]
    count = 1
    if len(args) == 2:
        try:
            count = int(args[1])
            if count < 0:
                return "ERR - value is not an integer or out of range"
        except ValueError:
            return "ERR - value is not an integer or out of range"

    res = db.zpopmin(key, count)
    return format_zset_response(res)

def zpopmax_command(db, args):
    if len(args) < 1 or len(args) > 2:
        return "ERR - wrong number of args"
    key = args[0]
    count = 1
    if len(args) == 2:
        try:
            count = int(args[1])
            if count < 0:
                return "ERR - value is not an integer or out of range"
        except ValueError:
            return "ERR - value is not an integer or out of range"

    res = db.zpopmax(key, count)
    return format_zset_response(res)
