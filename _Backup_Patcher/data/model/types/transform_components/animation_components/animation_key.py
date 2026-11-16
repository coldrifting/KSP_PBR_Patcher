from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec2 import Vec2

class AnimationKey:
    def __init__(self):
        self.time: float | int = 0
        self.value: float | int = 0
        self.tangent_in_out: Vec2 = Vec2(0, 0)
        self.tangent_mode: int = 0

    def read(self, reader: ByteReader) -> 'AnimationKey':
        self.time = reader.read_float()
        self.value = reader.read_float()
        self.tangent_in_out = reader.read_vec2()
        self.tangent_mode = reader.read_int()

        return self

    def write(self, writer: ByteWriter):
        writer.write_float(self.time)
        writer.write_float(self.value)
        writer.write_vec2(self.tangent_in_out)
        writer.write_int(self.tangent_mode)
