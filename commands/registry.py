from commands.string import *

COMMANDS = {
    "SET": set_command,
    "GET": get_command,
    "DEL": del_command,
    "PING": ping_command,
    "FLUSH": flush_command,
    "EXISTS": exists_command,
    "INCR": incr_command,
    "DECR": decr_command,
    "APPEND": append_command,
}

def execute(command, db, args):
    command = command.upper()

    if command not in COMMANDS:
        raise Exception("Unknown command")
    
    return COMMANDS[command](db, args)

def register(name, handler):
    COMMANDS[name.upper()] = handler