from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter


class Friction:
    def __init__(self):
        self.extremum_slip: float | int
        self.extremum_value: float | int
        self.asymptote_slip: float | int
        self.asymptote_value: float | int
        self.stiffness: float | int

    def read(self, reader: ByteReader) -> 'Friction':
        self.extremum_slip = reader.read_float()
        self.extremum_value = reader.read_float()
        self.asymptote_slip = reader.read_float()
        self.asymptote_value = reader.read_float()
        self.stiffness = reader.read_float()

        return self

    def write(self, writer: ByteWriter):
        writer.write_float(self.extremum_slip)
        writer.write_float(self.extremum_value)
        writer.write_float(self.asymptote_slip)
        writer.write_float(self.asymptote_value)
        writer.write_float(self.stiffness)
