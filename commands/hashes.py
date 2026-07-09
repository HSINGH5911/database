def hset_command(db, args):
    key = args[0]
    field = args[1]
    value = args[2]

    db.hset(key, field, value)

    return "OK"

def hget_command(db, args):
    key = args[0]
    field = args[1]

    return db.hget(key, field)

def hgetall_command(db, args):
    key = args[0]

    return db.hgetall(key)

def hdel_command(db, args):
    key = args[0]
    fields = args[1:]

    return db.hdel(key, fields)

def hincrby_command(db, args):
    key = args[0]
    field = args[1]
    incr = args[2]

    return db.hincrby(key, field, incr)

def hdecrby_command(db, args):
    key = args[0]
    field = args[1]
    decr = args[2]

    return db.hdecrby(key, field, decr)

def hexists_command(db, args):
    key = args[0]
    field = args[1]

    return db.hexists(key, field)
