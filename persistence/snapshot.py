import os
import json
import time
import threading
from core.database import SortedSet
from core.errors import PersistenceError

MAGIC_HEADER = "REDIS0001"

class RDBSnapshot:
    """RDB Snapshotting engine for saving and restoring database state."""

    _last_save_time = 0
    _saving_lock = threading.Lock()
    _is_saving = False

    def __init__(self, filepath="dump.rdb"):
        self.filepath = filepath

    @classmethod
    def get_last_save_time(cls):
        return cls._last_save_time

    def save(self, db):
        """Synchronously dumps the in-memory database state to an RDB snapshot file atomically."""
        with RDBSnapshot._saving_lock:
            RDBSnapshot._is_saving = True
            try:
                snapshot_data = {
                    "magic": MAGIC_HEADER,
                    "created_at": time.time(),
                    "keys_count": len(db.data),
                    "keys": {}
                }

                for key, val in db.data.items():
                    if isinstance(val, str):
                        snapshot_data["keys"][key] = {
                            "type": "string",
                            "value": val
                        }
                    elif isinstance(val, dict):
                        snapshot_data["keys"][key] = {
                            "type": "hash",
                            "value": val
                        }
                    elif isinstance(val, list):
                        snapshot_data["keys"][key] = {
                            "type": "list",
                            "value": val
                        }
                    elif isinstance(val, set):
                        snapshot_data["keys"][key] = {
                            "type": "set",
                            "value": list(val)
                        }
                    elif isinstance(val, SortedSet):
                        snapshot_data["keys"][key] = {
                            "type": "zset",
                            "value": dict(val.mapping)
                        }
                    else:
                        snapshot_data["keys"][key] = {
                            "type": "string",
                            "value": str(val)
                        }

                tmp_filepath = self.filepath + ".tmp"
                try:
                    with open(tmp_filepath, "w", encoding="utf-8") as f:
                        json.dump(snapshot_data, f, indent=2)
                        f.flush()
                        os.fsync(f.fileno())

                    os.replace(tmp_filepath, self.filepath)
                    RDBSnapshot._last_save_time = int(snapshot_data["created_at"])
                    return len(snapshot_data["keys"])
                except Exception as e:
                    if os.path.exists(tmp_filepath):
                        try:
                            os.remove(tmp_filepath)
                        except OSError:
                            pass
                    raise PersistenceError(f"Failed to save RDB snapshot: {e}")
            finally:
                RDBSnapshot._is_saving = False

    def bgsave(self, db):
        """Spawns a background thread to execute RDB snapshot saving asynchronously."""
        with RDBSnapshot._saving_lock:
            if RDBSnapshot._is_saving:
                return "ERR Background save already in progress"

        thread = threading.Thread(
            target=self._bgsave_worker,
            args=(db,),
            daemon=True
        )
        thread.start()
        return "Background saving started"

    def _bgsave_worker(self, db):
        try:
            self.save(db)
        except Exception as e:
            print(f"[!] BGSAVE failed: {e}")

    def load(self, db):
        """Reads RDB snapshot file and restores all key-value entries into the database."""
        if not os.path.exists(self.filepath):
            return 0

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                snapshot_data = json.load(f)
        except Exception as e:
            raise PersistenceError(f"Corrupt or invalid RDB snapshot file: {e}")

        if not isinstance(snapshot_data, dict) or snapshot_data.get("magic") != MAGIC_HEADER:
            raise PersistenceError("Invalid RDB snapshot magic header or format")

        keys_dict = snapshot_data.get("keys", {})
        loaded_count = 0

        for key, item in keys_dict.items():
            val_type = item.get("type")
            val = item.get("value")

            if val_type == "string":
                db.data[key] = str(val)
            elif val_type == "hash":
                db.data[key] = dict(val)
            elif val_type == "list":
                db.data[key] = list(val)
            elif val_type == "set":
                db.data[key] = set(val)
            elif val_type == "zset":
                zset = SortedSet()
                if isinstance(val, dict):
                    for member, score in val.items():
                        zset.add(member, score)
                db.data[key] = zset
            else:
                db.data[key] = str(val)

            loaded_count += 1

        print(f"[*] RDB Load complete: Loaded {loaded_count} keys from '{self.filepath}'.")
        return loaded_count
