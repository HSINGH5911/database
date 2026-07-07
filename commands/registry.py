from commands.string import *

COMMANDS = {
    "SET": set_command,
    "GET": get_command,
    "DEL": del_command,
    "PING": ping_command,
    "FLUSH": flush_command
}

def execute(command, db, args):
    command = command.upper()

    if command not in COMMANDS:
        return "ERROR"
    
    return COMMANDS[command](db, args)

