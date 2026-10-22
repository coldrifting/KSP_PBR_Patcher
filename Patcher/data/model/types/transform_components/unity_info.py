from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.generic.mu_component import MuComponent
from data.model.types.tag.tag_mu import MuTag


class UnityInfo(MuComponent):
    def __init__(self, tag: str, layer: int):
        self.tag: str = tag
        self.layer: int = layer

    @staticmethod
    def read(reader: ByteReader) -> 'UnityInfo':
        tag: str = reader.read_str()
        layer: int = reader.read_int()

        return UnityInfo(tag=tag, layer=layer)

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.UnityInfo)

        writer.write_str(self.tag)
        writer.write_int(self.layer)
