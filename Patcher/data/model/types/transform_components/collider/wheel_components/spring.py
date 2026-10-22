from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter


class Spring:
    def __init__(self):
        self.spring: float
        self.damper: float
        self.target_pos: float

    def read(self, reader: ByteReader) -> 'Spring':
        self.spring = reader.read_float()
        self.damper = reader.read_float()
        self.target_pos = reader.read_float()

        return self

    def write(self, writer: ByteWriter):
        writer.write_float(self.spring)
        writer.write_float(self.damper)
        writer.write_float(self.target_pos)
