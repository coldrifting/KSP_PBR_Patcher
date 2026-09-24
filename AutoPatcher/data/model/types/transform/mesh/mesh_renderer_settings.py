from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.mu_tag import MuTag

class MeshRendererSettings:
    def __init__(self, cast_shadows: bool, receive_shadows: bool, material_count: int, material_index: int):
        self.cast_shadows = cast_shadows
        self.receive_shadows = receive_shadows
        self.material_count = material_count
        self.material_index = material_index

    def clone(self):
        return MeshRendererSettings(
            cast_shadows=self.cast_shadows,
            receive_shadows=self.receive_shadows,
            material_count=self.material_count,
            material_index=self.material_index
        )

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshRenderer)
        writer.write_bool(self.cast_shadows)
        writer.write_bool(self.receive_shadows)
        writer.write_int(self.material_count)
        writer.write_int(self.material_index)

    @staticmethod
    def read(reader: ByteReader) -> 'MeshRendererSettings':
        reader.read_int()  # Consume Tag
        cast_shadows = reader.read_bool()
        receive_shadows = reader.read_bool()
        material_count = reader.read_int()
        material_index = reader.read_int()

        return MeshRendererSettings(
            cast_shadows = cast_shadows,
            receive_shadows = receive_shadows,
            material_count = material_count,
            material_index = material_index
        )