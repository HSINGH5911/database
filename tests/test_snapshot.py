import os
import time
import unittest
from core.database import Database, SortedSet
from core.errors import PersistenceError
from persistence.snapshot import RDBSnapshot
from persistence.loader import Loader
from commands.registry import execute

TEST_RDB_FILE = "test_dump.rdb"
TEST_AOF_FILE = "test_dump.aof"

class TestRDBSnapshot(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        self.rdb = RDBSnapshot(filepath=TEST_RDB_FILE)
        self._cleanup()

    def tearDown(self):
        self._cleanup()

    def _cleanup(self):
        for path in [TEST_RDB_FILE, TEST_RDB_FILE + ".tmp", TEST_AOF_FILE]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass

    def test_save_and_load_all_types(self):
        # 1. Populate DB with various data types
        self.db.set("str_key", "hello world")
        self.db.hset("hash_key", "f1", "v1")
        self.db.hset("hash_key", "f2", "v2")
        self.db.rpush("list_key", "item1", "item2", "item3")
        self.db.sadd("set_key", "m1", "m2")
        self.db.zadd("zset_key", [("10.5", "user1"), ("20.0", "user2")])

        # 2. Save snapshot
        keys_saved = self.rdb.save(self.db)
        self.assertEqual(keys_saved, 5)
        self.assertTrue(os.path.exists(TEST_RDB_FILE))

        # 3. Create fresh DB and load snapshot
        new_db = Database()
        keys_loaded = self.rdb.load(new_db)
        self.assertEqual(keys_loaded, 5)

        # 4. Verify data integrity across types
        self.assertEqual(new_db.get("str_key"), "hello world")
        self.assertEqual(new_db.hgetall("hash_key"), {"f1": "v1", "f2": "v2"})
        self.assertEqual(new_db.lrange("list_key", 0, -1), ["item1", "item2", "item3"])
        self.assertEqual(new_db.smembers("set_key"), {"m1", "m2"})
        self.assertIsInstance(new_db.get("zset_key") if hasattr(new_db, "get") else new_db.data["zset_key"], SortedSet)
        self.assertEqual(new_db.zscore("zset_key", "user1"), "10.5")
        self.assertEqual(new_db.zscore("zset_key", "user2"), "20")

    def test_bgsave(self):
        self.db.set("key1", "val1")
        res = self.rdb.bgsave(self.db)
        self.assertIn("Background saving started", res)
        
        # Wait briefly for worker thread
        time.sleep(0.2)
        self.assertTrue(os.path.exists(TEST_RDB_FILE))

    def test_load_non_existent_file(self):
        non_existent_rdb = RDBSnapshot("non_existent_dump.rdb")
        loaded = non_existent_rdb.load(self.db)
        self.assertEqual(loaded, 0)

    def test_load_corrupt_file(self):
        with open(TEST_RDB_FILE, "w") as f:
            f.write("invalid json content")

        with self.assertRaises(PersistenceError):
            self.rdb.load(self.db)

    def test_commands(self):
        self.db.set("cmd_key", "cmd_val")
        res_save = execute("SAVE", self.db, [])
        self.assertEqual(res_save, "OK")

        res_bgsave = execute("BGSAVE", self.db, [])
        self.assertEqual(res_bgsave, "Background saving started")

        res_lastsave = execute("LASTSAVE", self.db, [])
        self.assertTrue(res_lastsave.startswith("(integer)"))

    def test_loader_integration(self):
        self.db.set("k1", "v1")
        self.rdb.save(self.db)

        restored_db = Database()
        loader = Loader(restored_db, rdb_filepath=TEST_RDB_FILE, aof_filepath=TEST_AOF_FILE)
        count = loader.load()
        self.assertEqual(count, 1)
        self.assertEqual(restored_db.get("k1"), "v1")

if __name__ == "__main__":
    unittest.main()
