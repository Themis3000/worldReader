import io
import struct
import zlib
from typing import List


class MCA:
    def __init__(self, data: bytes):
        self.data = io.BytesIO(data)
        self.chunks: List[Chunk] = []
        self._load_data()
        del self.data

    def _load_data(self):
        locations = []
        # Iterate through each location
        for i in range(1024):
            location_offset_raw = self.data.read(3)
            location_sector_count_raw = self.data.read(1)
            location_offset = int.from_bytes(location_offset_raw, "big")
            location_sector_count = int.from_bytes(location_sector_count_raw, "big")
            locations.append([location_offset, location_sector_count])

        for [location_offset, location_sector_count] in locations:
            if location_offset == 0 and location_sector_count == 0:
                # If both are 0, this chunk has not yet been generated
                continue
            # Offset and sector count are in increments of 4KiB
            self.data.seek(location_offset*4096)
            # The sector count is rounded up, some data in the tail end will be garbage.
            chunk_raw = self.data.read(location_sector_count*4096)
            chunk = Chunk(chunk_raw)
            self.chunks.append(chunk)


class Chunk:
    def __init__(self, data: bytes):
        self.data = io.BytesIO(data)
        self.nbt_data = None
        self._load_data()
        del self.data

    def _load_data(self):
        length_raw = self.data.read(4)
        length = int.from_bytes(length_raw, "big")
        compression_type = self.data.read(1)
        if compression_type != b"\x02":
            raise Exception("Unsupported compression type found.")
        # The compression type is part of the length, so 1 must be subtracted.
        chunk_data_raw_compressed = self.data.read(length-1)
        chunk_data_raw = zlib.decompress(chunk_data_raw_compressed)
        self.nbt_data = NBT(chunk_data_raw).__dict__()


class NBT:
    def __init__(self, data):
        self.data = io.BytesIO(data)
        self._load_data()

    def __dict__(self):
        return self.nbt

    def _load_data(self):
        name, data = self._decode_tags()
        self.nbt = data
        del self.data

    # It is assumed that this function is ran when the pointer is right behind a tag
    # This function will additionally return None when an END tag is encountered
    def _decode_tags(self, has_name=True, tag_type=None):
        # Read and set tag type if it is not defined
        if tag_type is None:
            tag_type_raw = self.data.read(1)
            tag_type = int.from_bytes(tag_type_raw, "big")
        # End tag has no name and no data.
        if tag_type == 0:
            return None, None
        if has_name:
            name_length_raw = self.data.read(2)
            name_length = int.from_bytes(name_length_raw, "big", signed=False)
            name_raw = self.data.read(name_length)
            name = name_raw.decode("utf-8")
        match tag_type:
            # Byte
            case 1:
                data_raw = self.data.read(1)
                data = int.from_bytes(data_raw, "big", signed=True)
            # Short
            case 2:
                data_raw = self.data.read(2)
                data = int.from_bytes(data_raw, "big", signed=True)
            # Int
            case 3:
                data_raw = self.data.read(4)
                data = int.from_bytes(data_raw, "big", signed=True)
            # Long
            case 4:
                data_raw = self.data.read(8)
                data = int.from_bytes(data_raw, "big", signed=True)
            # Float
            case 5:
                data_raw = self.data.read(4)
                [data] = struct.unpack(">f", data_raw)
            # double
            case 6:
                data_raw = self.data.read(8)
                [data] = struct.unpack(">d", data_raw)
            # byte array
            case 7:
                size_raw = self.data.read(4)
                size = int.from_bytes(size_raw, "big", signed=True)
                out = []
                for i in range(size):
                    byte_raw = self.data.read(1)
                    byte = int.from_bytes(byte_raw, "big", signed=True)
                    out.append(byte)
                data = out
            # string
            case 8:
                length_raw = self.data.read(2)
                length = int.from_bytes(length_raw, "big", signed=False)
                data_raw = self.data.read(length)
                data = data_raw.decode("utf-8")
            # list
            case 9:
                tag_id_raw = self.data.read(1)
                tag_id = int.from_bytes(tag_id_raw, "big", signed=True)
                size_raw = self.data.read(4)
                size = int.from_bytes(size_raw, "big", signed=True)
                out = []
                for i in range(size):
                    list_element = self._decode_tags(has_name=False, tag_type=tag_id)
                    out.append(list_element)
                data = out
            # compound
            case 10:
                out = {}
                while True:
                    compound_name, compound_data = self._decode_tags()
                    # No name/no data marks the end of the compound.
                    if compound_name is None and compound_data is None:
                        break
                    out[compound_name] = compound_data
                data = out
            # int array
            case 11:
                size_raw = self.data.read(4)
                size = int.from_bytes(size_raw, "big", signed=True)
                out = []
                for i in range(size):
                    list_element_raw = self.data.read(4)
                    list_element = int.from_bytes(list_element_raw, "big", signed=True)
                    out.append(list_element)
                data = out
            # long array
            case 12:
                size_raw = self.data.read(4)
                size = int.from_bytes(size_raw, "big", signed=True)
                out = []
                for i in range(size):
                    list_element_raw = self.data.read(8)
                    list_element = int.from_bytes(list_element_raw, "big", signed=True)
                    out.append(list_element)
                data = out
            case _:
                raise Exception("Invalid tag type found in NBT data.")

        if has_name:
            return name, data
        return data
