from core.database import Database
from commands.registry import execute

db = Database()

while True:
    command_line = input("redis> ")

    parts = command_line.split()

    command = parts[0]
    args = parts[1:]

    result = execute(command, db, args)

    print(result)