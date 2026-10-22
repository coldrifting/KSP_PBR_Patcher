from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec3 import Vec3
from data.model.types.tag.tag_mu import MuTag
from data.model.types.transform_components.mesh_components.base import MuMeshComponent


class MeshNormals(MuMeshComponent):
    def __init__(self, normals: list[Vec3]):
        self.normals: list[Vec3] = normals

    def __str__(self):
        return f"Normals: {len(self.normals)}"

    @staticmethod
    def read(reader: ByteReader, num_vertices: int) -> 'MeshNormals':
        normals: list[Vec3] = []
        for _ in range(num_vertices):
            normals.append(reader.read_vec3())

        return MeshNormals(normals=normals)

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshNormals)

        for vertex in self.normals:
            writer.write_vec3(vertex)

    # Modifications
    def delete(self, indices: set[int]):
        for i in reversed(range(len(self.normals))):
            if i in indices:
                del self.normals[i]

    def paste(self, pasted_normals: 'MeshNormals'):
        for normal in pasted_normals.normals:
            self.normals.append(normal)
