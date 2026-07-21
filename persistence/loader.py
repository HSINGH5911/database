import os
from persistence.aof import AOFLogger

class Loader:
    def __init__(self, db, aof_filepath="appendonly.aof"):
        self.db = db
        self.aof_filepath = aof_filepath

    def load(self):
        """Loads and reconstructs database state from persistent AOF log on startup."""
        if os.path.exists(self.aof_filepath):
            aof = AOFLogger(filepath=self.aof_filepath)
            count = aof.load_and_replay(self.db)
            aof.close()
            return count
        return 0
