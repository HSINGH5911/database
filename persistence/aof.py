import os
from protocol.serializer import Serializer
from protocol.parser import Parser
from commands.registry import execute

WRITE_COMMANDS = {
    "SET", "DEL", "FLUSH", "FLUSHALL", "FLUSHDB", "INCR", "DECR", "APPEND",
    "HSET", "HDEL", "HINCRBY", "HDECRBY",
    "LPUSH", "RPUSH", "LPOP", "RPOP", "LREM", "LTRIM", "RPOPLPUSH", "LMOVE",
    "SADD", "SREM", "SPOP", "SMOVE", "SINTERSTORE", "SUNIONSTORE", "SDIFFSTORE",
    "ZADD", "ZREM", "ZINCRBY", "ZPOPMIN", "ZPOPMAX",
    "RENAME", "RENAMENX"
}

class AOFLogger:
    def __init__(self, filepath="appendonly.aof"):
        self.filepath = filepath
        self.file = open(self.filepath, "a+", encoding="utf-8", newline="")

    def log(self, command, args):
        """Appends a write command to the AOF log file in RESP format."""
        cmd_upper = command.upper()
        if cmd_upper not in WRITE_COMMANDS:
            return  # Skip read-only commands

        payload = [cmd_upper] + list(args)
        resp_data = Serializer.array(payload)
        self.file.write(resp_data)
        self.file.flush()

    def load_and_replay(self, db):
        """Reads AOF file and replays all commands sequentially to restore DB state."""
        if not os.path.exists(self.filepath):
            return 0

        self.file.seek(0)
        content = self.file.read()

        if not content.strip():
            return 0

        parser = Parser()
        blocks = [block for block in content.split("*") if block.strip()]

        replayed_count = 0
        for block in blocks:
            resp_payload = "*" + block
            tokens = parser.parse(resp_payload)

            if tokens:
                cmd = tokens[0]
                args = tokens[1:]
                execute(cmd, db, args)
                replayed_count += 1

        print(f"[*] AOF Replay complete: Replayed {replayed_count} write commands.")
        return replayed_count

    def close(self):
        if self.file:
            self.file.close()