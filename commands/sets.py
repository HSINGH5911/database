def sadd_command(db, args):
    key = args[0]
    members = args[1:]

    return db.sadd(key, *members)

def srem_command(db, args):
    key = args[0]
    members = args[1:]

    return db.srem(key, *members)

def spop_command(db, args):
    key = args[0]

    if len(args) > 1:
        count = args[1]
        return db.spop(key, count)

    return db.spop(key)

