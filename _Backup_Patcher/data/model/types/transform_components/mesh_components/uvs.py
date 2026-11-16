from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec2 import Vec2
from data.model.types.tag.tag_mu import MuTag
from data.model.types.transform_components.mesh_components.base import MuMeshComponent


class MeshUvs(MuMeshComponent):
    def __init__(self, uvs: list[Vec2], is_uv2: bool):
        self.uvs: list[Vec2] = uvs
        self.is_uv2: bool = is_uv2

    @staticmethod
    def read(reader: ByteReader, num_vertices: int, is_uv2: bool) -> 'MeshUvs':
        uvs: list[Vec2] = []
        for _ in range(num_vertices):
            uv = reader.read_vec2()
            uvs.append(uv)

        return MeshUvs(uvs=uvs, is_uv2=is_uv2)

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshUv2 if self.is_uv2 else MuTag.MeshUv)

        for uv in self.uvs:
            writer.write_vec2(uv)

    def __str__(self):
        return f"Uv{'2' if self.is_uv2 else ''}s: {len(self.uvs)}"

    # Modifications
    def delete(self, indices: set[int]):
        for i in reversed(range(len(self.uvs))):
            if i in indices:
                del self.uvs[i]

    def paste(self, pasted_uvs: 'MeshUvs'):
        for uv in pasted_uvs.uvs:
            self.uvs.append(uv)
