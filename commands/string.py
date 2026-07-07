def set_command(db, args):
    key = args[0]
    value = args[1]

    db.set(key, value)
    return "OK"

def get_command(db, args):
    key = args[0]

    value = db.get(key)

    if value is None:
        return "(nil)"
    
    return value

def del_command(db, args):
    key = args[0]

    success = db.delete(key)

    return success

def ping_command(db, args):
    return "PONG"

def flush_command(db, args):
    db.flush()

    return "OK"

def exists_command(db, args):
    return db.exists(args[0])

def incr_command(db, args):
    if len(args) != 1:
        return "ERR - wrong number of args"
    return db.incr(args[0])

def decr_command(db, args):
    if len(args) != 1:
        return "ERR - wrong number of args"
    return db.decr(args[0])

def append_command(db, args):
    key = args[0]
    message = args[1]

    return db.append(key, message)

