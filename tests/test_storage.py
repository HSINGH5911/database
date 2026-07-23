import unittest
from core.storage import SortedPage, PageAllocator, MemoryStorageBackend, PAGE_SIZE

class TestStorage(unittest.TestCase):
    def test_sorted_page_crud(self):
        page = SortedPage(page_id=0, page_size=PAGE_SIZE)
        payload = b"Hello, World!"
        
        slot_id = page.insert_record(payload)
        self.assertIsNotNone(slot_id)
        
        read_bytes = page.read_record(slot_id)
        self.assertEqual(read_bytes, payload)

        self.assertTrue(page.delete_record(slot_id))
        self.assertIsNone(page.read_record(slot_id))

    def test_page_allocator(self):
        allocator = PageAllocator()
        p1 = allocator.allocate_page()
        p2 = allocator.allocate_page()
        self.assertEqual(p1.page_id, 0)
        self.assertEqual(p2.page_id, 1)

        allocator.free_page(p1.page_id)
        p3 = allocator.allocate_page()
        self.assertEqual(p3.page_id, 0)  # Recycled

    def test_memory_storage_backend(self):
        backend = MemoryStorageBackend()
        self.assertTrue(backend.set("user:100", "Alice"))
        self.assertEqual(backend.get("user:100"), "Alice")

        stats = backend.stats()
        self.assertEqual(stats["total_keys"], 1)
        self.assertGreater(stats["utilized_bytes"], 0)

        self.assertTrue(backend.delete("user:100"))
        self.assertIsNone(backend.get("user:100"))

if __name__ == "__main__":
    unittest.main()
