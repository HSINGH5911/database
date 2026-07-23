import struct 
from typing import Dict, Tuple, Optional, List

PAGE_SIZE = 4096
HEADER_SIZE = 12
SLOT_SIZE  = 4
HEADER_FORMAT = ">IHH"
SLOT_FORMAT = ">HH"

class SortedPage:
    def __init__(self, page_id: int, page_size: int = PAGE_SIZE):
        self.page_id = page_id
        self.page_size = page_size
        self.buffer = bytearray(page_size)
        self.num_slots = 0
        self.free_space_offset = page_size
        self._write_header()

    def _write_header(self):
        struct.pack_into(HEADER_FORMAT, self.buffer, 0, self.page_id, self.num_slots, self.free_space_offset)

    def _read_header(self):
        self.page_id, self.num_slots, self.free_space_offset = struct.unpack_from(HEADER_FORMAT, self.buffer, 0)

    @property
    def free_space_bytes(self) -> int:
        slot_dir_end = HEADER_SIZE + (self.num_slots * SLOT_SIZE)
        return self.free_space_offset - slot_dir_end

    def can_fit(self, data_len: int) -> bool:
        needed = data_len + SLOT_SIZE
        return self.free_space_bytes >= needed

    def insert_record(self, data: bytes) -> Optional[int]:
        data_len = len(data)

        target_slot_id = None
        for s_id in range(self.num_slots):
            offset, length = struct.unpack_from(SLOT_FORMAT, self.buffer, HEADER_SIZE + (s_id * SLOT_SIZE))
            if length == 0:
                target_slot_id = s_id
                break

        needed_bytes = data_len if target_slot_id is not None else data_len + SLOT_SIZE
        if self.free_space_bytes < needed_bytes:
            return None

        new_offset = self.free_space_offset - data_len
        self.buffer[new_offset:new_offset + data_len] = data
        self.free_space_offset = new_offset

        if target_slot_id is not None:
            slot_id = target_slot_id
        else:
            slot_id = self.num_slots
            self.num_slots += 1

        struct.pack_into(SLOT_FORMAT, self.buffer, HEADER_SIZE + (slot_id * SLOT_SIZE), new_offset, data_len)
        self._write_header()
        return slot_id

    def read_record(self, slot_id: int) -> Optional[bytes]:
        if slot_id < 0 or slot_id >= self.num_slots:
            return None

        offset, length = struct.unpack_from(SLOT_FORMAT, self.buffer, HEADER_SIZE + (slot_id * SLOT_SIZE))
        if length == 0:
            return None

        return bytes(self.buffer[offset:offset + length])

    def delete_record(self, slot_id: int) -> bool:
        if slot_id < 0 or slot_id >= self.num_slots:
            return False

        offset, length = struct.unpack_from(SLOT_FORMAT, self.buffer, HEADER_SIZE + (slot_id * SLOT_SIZE))
        if length == 0:
            return False

        struct.pack_into(SLOT_FORMAT, self.buffer, HEADER_SIZE + (slot_id * SLOT_SIZE), 0, 0)
        self._write_header()
        return True

    def compact(self):
        active_records = []
        for s_id in range(self.num_slots):
            offset, length = struct.unpack_from(SLOT_FORMAT, self.buffer, HEADER_SIZE + (s_id * SLOT_SIZE))
            if length > 0:
                payload = bytes(self.buffer[offset:offset + length])         
                active_records.append((s_id, payload))

        self.free_space_offset = self.page_size
        for s_id, payload in active_records:
            data_len = len(payload)
            new_offset = self.free_space_offset - data_len
            self.buffer[new_offset:new_offset + data_len] = payload
            self.free_space_offset = new_offset
            struct.pack_into(SLOT_FORMAT, self.buffer, HEADER_SIZE + (s_id * SLOT_SIZE), new_offset, data_len)

        self._write_header()


class PageAllocator:
    """
    Manages allocation, tracking, and recycling of memory pages.
    """
    def __init__(self, page_size: int = PAGE_SIZE):
        self.page_size = page_size
        self.pages: Dict[int, SortedPage] = {}
        self.free_page_ids: List[int] = []
        self._next_page_id = 0

    def allocate_page(self) -> SortedPage:
        """Allocates a new page or reuses a freed page ID."""
        if self.free_page_ids:
            page_id = self.free_page_ids.pop()
        else:
            page_id = self._next_page_id
            self._next_page_id += 1

        page = SortedPage(page_id=page_id, page_size=self.page_size)
        self.pages[page_id] = page
        return page

    def get_page(self, page_id: int) -> Optional[SortedPage]:
        """Retrieves page by ID."""
        return self.pages.get(page_id)

    def free_page(self, page_id: int) -> bool:
        """Deallocates a page and returns its ID to the freelist."""
        if page_id in self.pages:
            del self.pages[page_id]
            self.free_page_ids.append(page_id)
            return True
        return False


class MemoryStorageBackend:
    """
    Custom memory storage backend using block/page allocation.
    """
    def __init__(self, page_size: int = PAGE_SIZE):
        self.allocator = PageAllocator(page_size=page_size)
        self.index: Dict[str, Tuple[int, int]] = {}  # key -> (page_id, slot_id)

    def set(self, key: str, value: str) -> bool:
        """Stores key-value pair in page storage."""
        payload = value.encode('utf-8')

        # If key exists, delete existing slot reference first
        if key in self.index:
            self.delete(key)

        # Find existing page with free space
        target_page = None
        for page in self.allocator.pages.values():
            if page.can_fit(len(payload)):
                target_page = page
                break

        # Allocate new page if no page fits
        if target_page is None:
            target_page = self.allocator.allocate_page()

        slot_id = target_page.insert_record(payload)
        if slot_id is None:
            target_page.compact()
            slot_id = target_page.insert_record(payload)

        if slot_id is not None:
            self.index[key] = (target_page.page_id, slot_id)
            return True

        return False

    def get(self, key: str) -> Optional[str]:
        """Retrieves value by key."""
        rid = self.index.get(key)
        if not rid:
            return None

        page_id, slot_id = rid
        page = self.allocator.get_page(page_id)
        if not page:
            return None

        data = page.read_record(slot_id)
        return data.decode('utf-8') if data else None

    def delete(self, key: str) -> bool:
        """Deletes key and frees slot in page."""
        rid = self.index.pop(key, None)
        if not rid:
            return False

        page_id, slot_id = rid
        page = self.allocator.get_page(page_id)
        if page:
            page.delete_record(slot_id)
            return True
        return False

    def stats(self) -> dict:
        """Returns memory and allocation stats."""
        total_pages = len(self.allocator.pages)
        total_capacity = total_pages * PAGE_SIZE
        total_free = sum(p.free_space_bytes for p in self.allocator.pages.values())
        return {
            "total_pages": total_pages,
            "total_capacity_bytes": total_capacity,
            "free_space_bytes": total_free,
            "utilized_bytes": total_capacity - total_free,
            "total_keys": len(self.index)
        }
