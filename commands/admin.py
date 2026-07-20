import time

def format_admin_response(res):
    if res is None:
        return "(nil)"
    if isinstance(res, str) and (res.startswith("WRONGTYPE") or res.startswith("ERR")):
        return res
    if isinstance(res, bool):
        return "OK" if res else "ERR - no such key"
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

def dbsize_command(db, args):
    if len(args) != 0:
        return "ERR - wrong number of args"
    res = db.dbsize()
    return format_admin_response(res)

def keys_command(db, args):
    pattern = args[0] if len(args) >= 1 else "*"
    res = db.keys(pattern)
    return format_admin_response(res)

def type_command(db, args):
    if len(args) != 1:
        return "ERR - wrong number of args"
    key = args[0]
    res = db.type(key)
    return format_admin_response(res)

def rename_command(db, args):
    if len(args) != 2:
        return "ERR - wrong number of args"
    key = args[0]
    newkey = args[1]
    res = db.rename(key, newkey)
    return format_admin_response(res)

def renamenx_command(db, args):
    if len(args) != 2:
        return "ERR - wrong number of args"
    key = args[0]
    newkey = args[1]
    res = db.renamenx(key, newkey)
    return format_admin_response(res)

def randomkey_command(db, args):
    if len(args) != 0:
        return "ERR - wrong number of args"
    res = db.randomkey()
    return format_admin_response(res)

def info_command(db, args):
    res = db.info()
    return format_admin_response(res)

def time_command(db, args):
    if len(args) != 0:
        return "ERR - wrong number of args"
    res = db.time()
    return format_admin_response(res)

def flushall_command(db, args):
    db.flush()
    return "OK"

def flushdb_command(db, args):
    db.flush()
    return "OK"
