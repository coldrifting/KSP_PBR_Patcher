import struct

from data.model.types.core.color_byte import ColorByte
from data.model.types.core.int2 import Int2
from data.model.types.core.int3 import Int3
from data.model.types.core.int4 import Int4
from data.model.types.core.vec2 import Vec2
from data.model.types.core.vec3 import Vec3
from data.model.types.core.vec4 import Vec4


class ByteReader:
    def __init__(self, input_bytes: bytes):
        self.input_bytes = input_bytes
        self.pointer: int = 0
        self.remaining: int = len(self.input_bytes)

    def __str__(self) -> str:
        return "Reader Index: " + hex(self.pointer)

    def has_data(self) -> bool:
        return self.remaining > 0

    def preview(self, num_bytes = 4) -> int:
        output = self.input_bytes[self.pointer:self.pointer + num_bytes]
        return int.from_bytes(output, byteorder='little')

    def read(self, size: int) -> bytes:
        output = self.input_bytes[self.pointer:self.pointer + size]
        self.pointer += size
        self.remaining -= size
        return output

    def read_bool(self) -> bool:
        output = self.read(1)
        return bool.from_bytes(output, byteorder='little')

    def read_byte(self) -> int:
        output = self.read(1)
        return int.from_bytes(output, byteorder='little')

    def read_int(self) -> int:
        output = self.read(4)
        return struct.unpack('i', output)[0]

    def read_uint(self) -> int:
        output = self.read(4)
        return struct.unpack('<I', output)[0]

    def read_float(self) -> int:
        output = self.read(4)
        return struct.unpack('f', output)[0]

    def read_color_byte(self) -> ColorByte:
        return ColorByte(
            r=self.read_byte(),
            g=self.read_byte(),
            b=self.read_byte(),
            a=self.read_byte()
        )

    def read_int2(self) -> Int2:
        return Int2(
            x=self.read_int(),
            y=self.read_int()
        )

    def read_int3(self) -> Int3:
        return Int3(
            x=self.read_int(),
            y=self.read_int(),
            z=self.read_int()
        )

    def read_int4(self) -> Int4:
        return Int4(
            x=self.read_int(),
            y=self.read_int(),
            z=self.read_int(),
            w=self.read_int()
        )

    def read_vec2(self) -> Vec2:
        return Vec2(
            x=self.read_float(),
            y=self.read_float()
        )

    def read_vec3(self) -> Vec3:
        return Vec3(
            x=self.read_float(),
            y=self.read_float(),
            z=self.read_float()
        )

    def read_vec4(self) -> Vec4:
        return Vec4(
            x=self.read_float(),
            y=self.read_float(),
            z=self.read_float(),
            w=self.read_float()
        )

    # Reads a variable length string with 1 or 2 bytes encoding the length
    def read_str(self) -> str:
        s1 = self.read_byte()
        if s1 >= 128:
            s2 = self.read_byte()
            length = (s2 * 128) + (s1 - 128)
        else:
            length = s1

        return self.read(length).decode('utf-8')