from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter


class MuComponent:
    def __str__(self) -> str:
        return type(self).__name__

    @staticmethod
    def read(reader: ByteReader):
        raise NotImplementedError()

    def write(self, writer: ByteWriter):
        raise NotImplementedError()
