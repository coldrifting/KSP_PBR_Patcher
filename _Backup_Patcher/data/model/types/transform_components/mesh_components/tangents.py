from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec4 import Vec4
from data.model.types.tag.tag_mu import MuTag
from data.model.types.transform_components.mesh_components.base import MuMeshComponent


class MeshTangents(MuMeshComponent):
    def __init__(self, tangents: list[Vec4]):
        self.tangents: list[Vec4] = tangents

    def __str__(self):
        return f"Tangents: {len(self.tangents)}"

    @staticmethod
    def read(reader: ByteReader, num_vertices: int) -> 'MeshTangents':
        tangents: list[Vec4] = []
        for i in range(num_vertices):
            tangents.append(reader.read_vec4())

        return MeshTangents(tangents=tangents)

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshTangents)
        for normal in self.tangents:
            writer.write_vec4(normal)

    # Modifications
    def delete(self, indices: set[int]):
        for i in reversed(range(len(self.tangents))):
            if i in indices:
                del self.tangents[i]

    def paste(self, pasted_tangents: 'MeshTangents'):
        for tangent in pasted_tangents.tangents:
            self.tangents.append(tangent)
