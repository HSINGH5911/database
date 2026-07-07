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