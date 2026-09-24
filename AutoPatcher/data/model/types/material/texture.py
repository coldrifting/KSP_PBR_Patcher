from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter


class Texture:
    def __init__(self, name: str, is_normal_map: bool):
        self.name = name
        self.is_normal_map = is_normal_map

    def __str__(self) -> str:
        return self.name

    def write(self, writer: ByteWriter):
        writer.write_str(self.name)
        writer.write_int(self.is_normal_map)

    @staticmethod
    def read(reader: ByteReader) -> 'Texture':
        name = reader.read_str()
        is_normal_map = bool(reader.read_int())

        return Texture(name, is_normal_map)