from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec2 import Vec2

class AnimKey:
    def __init__(self, time: float, value: float, tangent_in_out: Vec2, tangent_mode: int):
        self.time = time
        self.value = value
        self.tangent_in_out = tangent_in_out
        self.tangent_mode = tangent_mode

    def write(self, writer: ByteWriter):
        writer.write_float(self.time)
        writer.write_float(self.value)
        writer.write_vec2(self.tangent_in_out)
        writer.write_int(self.tangent_mode)

    @staticmethod
    def read(reader: ByteReader) -> 'AnimKey':
        time = reader.read_float()
        value = reader.read_float()
        tangent_in_out = reader.read_vec2()
        tangent_mode = reader.read_int()

        return AnimKey(
            time = time,
            value = value,
            tangent_in_out = tangent_in_out,
            tangent_mode = tangent_mode
        )