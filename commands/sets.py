def sadd_command(db, args):
    key = args[0]
    members = args[1:]

    return db.sadd(key, *members)

def srem_command(db, args):
    key = args[0]
    members = args[1:]

    return db.srem(key, *members)

def sismember_command(db, args):
    key = args[0]
    member = args[1]

    return db.sismember(key, member)

def smismember_command(db, args):
    key = args[0]
    members = args[1:]

    return db.smismember(key, members)

def scard_command(db, args):
    key = args[0]

    return db.scard(key)

def smembers_command(db, args):
    key = args[0]

    return db.smembers(key)

def spop_command(db, args):
    key = args[0]

    if len(args) > 1:
        count = args[1]
        return db.spop(key, count)

    return db.spop(key)

def srandommember_command(db, args):
    key = args[0]
    count = args[1]

    if len(args) > 1:
        count = args[1]
        return db.srandommember(key, count)
    
    return db.srandommember(key, count)

def smove_command(db, args):
    origin = args[0]
    destination = args[1]
    item = [2]

    return db.smove(origin, destination, item)

def sinter_command(db, args):
    keys = args[0:]

    return db.sinter(keys)

def sinterstore_command(db, args):
    dest = args[0]
    keys = args[1:]

    return db.sinterstore(dest, keys)

def sunion_command(db, args):
    keys = args[0:]

    return db.sunion(keys)

def sunionstore_command(db, args):
    dest = args[0]
    keys = args[1:]

    return db.sunionstore(dest, keys)

def sdiff_command(db, args):
    first_key = args[0]
    rest = args[1:]

    return db.sdiff(first_key, rest)

def sdiffstore_command(db, args):
    dest = args[0]
    keys = args[1:]

    return db.sdiffstore(dest, keys)