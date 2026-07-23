import os
from persistence.aof import AOFLogger
from persistence.snapshot import RDBSnapshot

class Loader:
    def __init__(self, db, rdb_filepath="dump.rdb", aof_filepath="appendonly.aof"):
        self.db = db
        self.rdb_filepath = rdb_filepath
        self.aof_filepath = aof_filepath

    def load(self):
        """Loads and reconstructs database state from RDB snapshot and AOF log on startup."""
        rdb_count = 0
        if os.path.exists(self.rdb_filepath):
            rdb = RDBSnapshot(filepath=self.rdb_filepath)
            rdb_count = rdb.load(self.db)

        aof_count = 0
        if os.path.exists(self.aof_filepath):
            aof = AOFLogger(filepath=self.aof_filepath)
            aof_count = aof.load_and_replay(self.db)
            aof.close()

        return rdb_count + aof_count
