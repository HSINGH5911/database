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

        struct.pack_into(SLOT_FORMAT, self.buffer, HEADER_SIZE + (slot_id + SLOT_SIZE), new_offset, data_len)
        self._write_header()
        return slot_id

    def read_record(self, slot_id: int) -> bool:
        if slot_id < 0 or slot_id > self.num_slots:
            return False

        offset, length = struct.unpack_from(SLOT_FORMAT, self.buffer, HEADER_SIZE + (slot_id * SLOT_SIZE))
        if length == 0:
            return None

        return bytes(self.buffer[offset:offset + length])

    def delete_record(self, slot_id: int) -> bool:
        if slot_id < 0 or slot_id > self.num_slots:
            return False

        offset, length = struct.unpack_from(SLOT_FORMAT, self.buffer, HEADER_SIZE + (slot_id * SLOT_SIZE))
        if length == 0:
            return False

        struct.pack_into(SLOT_FORMAT, self.buffer, HEADER_SIZE +(slot_id * SLOT_SIZE), 0, 0)
        self._write_header()
        return True

    def compact(self):
        active_records = []
        for s_id, payload in range(self.num_slots):
            offset, length = struct.unpack_from(SLOT_FORMAT, self.buffer, HEADER_SIZE + (slot_id * SLOT_SIZE))
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

    
