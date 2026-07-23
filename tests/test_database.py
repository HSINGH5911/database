import unittest
from core.database import Database, SortedSet

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def test_string_operations(self):
        self.db.set("name", "Alice")
        self.assertEqual(self.db.get("name"), "Alice")
        self.assertTrue(self.db.delete("name"))
        self.assertIsNone(self.db.get("name"))

    def test_sorted_set(self):
        zset = SortedSet()
        zset.add("user1", 10.5)
        zset.add("user2", 20.0)
        self.assertEqual(zset.get_score("user1"), 10.5)
        self.assertEqual(len(zset), 2)
        sorted_items = zset.get_sorted()
        self.assertEqual(sorted_items[0][0], "user1")
        self.assertEqual(sorted_items[1][0], "user2")
        self.assertTrue(zset.remove("user1"))
        self.assertEqual(len(zset), 1)

    def test_flush(self):
        self.db.set("k1", "v1")
        self.db.set("k2", "v2")
        self.db.flush()
        self.assertIsNone(self.db.get("k1"))
        self.assertIsNone(self.db.get("k2"))

if __name__ == "__main__":
    unittest.main()
