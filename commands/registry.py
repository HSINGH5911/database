from commands.string import *
from commands.hashes import *
from commands.lists import *
from commands.sets import *
from commands.sorted_sets import *

COMMANDS = {
    # STRING COMMANDS
    "SET": set_command,
    "GET": get_command,
    "DEL": del_command,
    "PING": ping_command,
    "FLUSH": flush_command,
    "EXISTS": exists_command,
    "INCR": incr_command,
    "DECR": decr_command,
    "APPEND": append_command,

    # HASH COMMANDS
    "HSET": hset_command,
    "HGET": hget_command,
    "HGETALL": hgetall_command,
    "HDEL": hdel_command,
    "HINCRBY": hincrby_command,
    "HDECRBY": hdecrby_command,
    "HEXISTS": hexists_command,

    # LIST COMMANDS
    "LPUSH": lpush_command,
    "RPUSH": rpush_command,
    "LPOP": lpop_command,
    "RPOP": rpop_command,
    "LREM": lrem_command,
    "LRIM": lrim_command,
    "LTRIM": ltrim_command,
    "LRANGE": lrange_command,
    "LINDEX": lindex_command,
    "LLEN": llen_command,
    "RPOPLPUSH": rpoplpush_command,
    "LMOVE": lmove_command,

    # SET COMMANDS
    "SADD": sadd_command,
    "SREM": srem_command,
    "SISMEMBER": sismember_command,
    "SMISMEMBER": smismember_command,
    "SCARD": scard_command,
    "SMEMBERS": smembers_command,
    "SPOP": spop_command,
    "SRANDOMMEMBER": srandommember_command,
    "SMOVE": smove_command,
    "SINTER": sinter_command,
    "SINTERSTORE": sinterstore_command,
    "SUNION": sunion_command,
    "SUNIONSTORE": sunionstore_command,
    "SDIFF": sdiff_command,
    "SDIFFSTORE": sdiffstore_command,

    # SORTED SET COMMANDS
    "ZADD": zadd_command,
    "ZREM": zrem_command,
    "ZSCORE": zscore_command,
    "ZINCRBY": zincrby_command,
    "ZCARD": zcard_command,
    "ZCOUNT": zcount_command,
    "ZRANGE": zrange_command,
    "ZREVRANGE": zrevrange_command,
    "ZRANGEBYSCORE": zrangebyscore_command,
    "ZRANK": zrank_command,
    "ZREVRANK": zrevrank_command,
    "ZPOPMIN": zpopmin_command,
    "ZPOPMAX": zpopmax_command,
}

def execute(command, db, args):
    command = command.upper()

    if command not in COMMANDS:
        raise Exception("Unknown command")
    
    return COMMANDS[command](db, args)

def register(name, handler):
    COMMANDS[name.upper()] = handler