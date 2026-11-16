from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.generic.mu_component import MuComponent
from data.model.types.tag.tag_mu import MuTag

class MeshRenderer(MuComponent):
    def __init__(self,
                 shadow_cast: bool,
                 shadow_receive: bool,
                 material_count: int,
                 material_index: int):
        self.shadow_cast: bool = shadow_cast
        self.shadow_receive: bool = shadow_receive
        self.material_count: int = material_count
        self.material_index: int = material_index

    @staticmethod
    def read(reader: ByteReader) -> 'MeshRenderer':
        shadow_cast: bool = True
        shadow_receive: bool = True

        if reader.mu_version >= 1:
            shadow_cast = reader.read_bool()
            shadow_receive = reader.read_bool()

        material_count: int = reader.read_int()
        material_index: int = reader.read_int()

        return MeshRenderer(shadow_cast=shadow_cast,
                            shadow_receive=shadow_receive,
                            material_count=material_count,
                            material_index=material_index)


    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshRenderer)

        writer.write_bool(self.shadow_cast)
        writer.write_bool(self.shadow_receive)
        writer.write_int(self.material_count)
        writer.write_int(self.material_index)
