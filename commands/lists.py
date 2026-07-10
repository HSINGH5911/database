def lpush_command(db, args):
    key = args[0]
    values = args[1:]

    return db.lpush(key, *values)

def rpush_command(db, args):
    key = args[0]
    values = args[1:]

    return db.rpush(key, *values)

def lpop_command(db, args):
    key = args[0]
    amount = args[1]

    return db.lpop(key, amount)

def rpop_command(db, args):
    key = args[0]
    amount = args[1]

    return db.rpop(key, amount)

def lrem_command(db, args):
    key = args[0]
    count = args[1]
    value = args[2]

    return db.lrem(key, count, value)

def lrim_command(db, args):
    key = args[0]
    start = args[1]
    stop = args[2]

    return db.lrim(key, start, stop)

def lrange_command(db, args):
    key = args[0]
    start = args[1]
    stop = args[2]

    return db.lrange(key, start, stop)

def lindex_command(db, args):
    key = args[0]
    index = args[1]

    return db.lindex(key, index)

def llen_command(db, args):
    key = args

    return db.llen(key)

def rpoplpush_command(db, args):
    source = args[0]
    destination = args[1]

    return db.rpoplpush(source, destination)

def lmove_command(db, args):
    source = args[0]
    destination = args[1]
    left_right_1 = args[2]
    left_right_2 = args[3]

    return db.lmove(source, destination, left_right_1, left_right_2)



