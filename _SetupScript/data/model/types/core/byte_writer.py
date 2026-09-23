import struct

from data.model.types.core.color_byte import ColorByte
from data.model.types.core.int2 import Int2
from data.model.types.core.int3 import Int3
from data.model.types.core.int4 import Int4
from data.model.types.core.vec2 import Vec2
from data.model.types.core.vec3 import Vec3
from data.model.types.core.vec4 import Vec4


class ByteWriter:
    def __init__(self, ref_data: bytes | None = None):
        self.output_data: bytes = b''

        # Used for checking import-export w/o changes does not change structure of file
        self.ref_data = ref_data
        self.ref_pointer: int = len(self.output_data) if self.ref_data is not None else -1
        self.ref_remaining: int = len(self.ref_data) - len(self.output_data) if self.ref_data is not None else -1

    def __str__(self) -> str:
        return "Writer Index: " + hex(self.ref_pointer)

    def write(self, value: bytes):
        if self.ref_data is not None:
            assert self.ref_data[self.ref_pointer:self.ref_pointer + len(value)] == value
            self.ref_pointer += len(value)
            self.ref_remaining -= len(value)

        self.output_data += value

    def write_bool(self, value: bool):
        self.write(value.to_bytes(1, byteorder='little'))

    def write_byte(self, value: int):
        if value > 255:
            raise Exception(f'Value {value} is too large to fit inside a single byte. Must be 255 or lower')

        self.write(value.to_bytes(1, byteorder='little'))

    def write_int(self, value: int):
        int_as_bytes = value.to_bytes(4, byteorder='little', signed=True)
        self.write(int_as_bytes)

    def write_uint(self, value: int):
        uint_as_bytes = value.to_bytes(4, byteorder='little', signed=False)
        self.write(uint_as_bytes)

    def write_float(self, value: float):
        packed: bytes = struct.pack('f', value)
        self.write(packed)

    def write_color_byte(self, value: ColorByte):
        self.write_byte(value.r)
        self.write_byte(value.g)
        self.write_byte(value.b)
        self.write_byte(value.a)

    def write_int2(self, value: Int2):
        self.write_int(value.x)
        self.write_int(value.y)

    def write_int3(self, value: Int3):
        self.write_int(value.x)
        self.write_int(value.y)
        self.write_int(value.z)

    def write_int4(self, value: Int4):
        self.write_int(value.x)
        self.write_int(value.y)
        self.write_int(value.z)
        self.write_int(value.w)

    def write_vec2(self, value: Vec2):
        self.write_float(value.x)
        self.write_float(value.y)

    def write_vec3(self, value: Vec3):
        self.write_float(value.x)
        self.write_float(value.y)
        self.write_float(value.z)

    def write_vec4(self, value: Vec4):
        self.write_float(value.x)
        self.write_float(value.y)
        self.write_float(value.z)
        self.write_float(value.w)

    # Reads a variable length string with 1 or 2 bytes encoding the length
    def write_str(self, value: str):
        output = b''
        if len(value) < 128:
            s1 = len(value)
            output += s1.to_bytes(1, byteorder='little')
        elif len(value) < 16384:
            s2 = (len(value) // 128)
            s1 = (len(value) % 128) + 128
            output += s1.to_bytes(1, byteorder='little')
            output += s2.to_bytes(1, byteorder='little')
        else:
            raise Exception(f"String Length too long: {len(value)}")

        output += value.encode('utf-8')
        self.write(output)