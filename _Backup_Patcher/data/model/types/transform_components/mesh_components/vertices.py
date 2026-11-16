from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec3 import Vec3
from data.model.types.tag.tag_mu import MuTag
from data.model.types.transform_components.mesh_components.base import MuMeshComponent


class MeshVertices(MuMeshComponent):
    def __init__(self, vertices: list[Vec3]):
        self.vertices: list[Vec3] = vertices

    def __str__(self):
        return f"Vertices: {len(self.vertices)}"

    @staticmethod
    def read(reader: ByteReader, num_vertices: int) -> 'MeshVertices':
        vertices: list[Vec3] = []

        for i in range(num_vertices):
            vertices.append(reader.read_vec3())

        return MeshVertices(vertices=vertices)

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshVertices)

        for vertex in self.vertices:
            writer.write_vec3(vertex)

    # Modifications
    def delete(self, indices: set[int]):
        for i in reversed(range(len(self.vertices))):
            if i in indices:
                del self.vertices[i]

    def paste(self, pasted_vertices: 'MeshVertices'):
        for vertex in pasted_vertices.vertices:
            self.vertices.append(vertex)
