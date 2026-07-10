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


