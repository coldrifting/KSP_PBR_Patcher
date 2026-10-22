from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.int3 import Int3
from data.model.types.tag.tag_mu import MuTag
from data.model.types.transform_components.mesh_components.base import MuMeshComponent


class MeshTriangles(MuMeshComponent):
    def __init__(self, triangles: list[Int3]):
        self.triangles: list[Int3] = triangles

    def __str__(self):
        return f"Triangles: {len(self.triangles)}"

    @staticmethod
    def read(reader: ByteReader) -> 'MeshTriangles':
        num_triangles = reader.read_int()
        triangles = []
        for _ in range(num_triangles // 3):
            triangles.append(reader.read_int3())

        return MeshTriangles(triangles=triangles)

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshTriangles)

        writer.write_int(len(self.triangles) * 3)
        for triangle in self.triangles:
            writer.write_int3(triangle)

    # Modifications
    def paste(self, pasted_triangles: 'MeshTriangles', num_vertices: int):
        for i in range(len(pasted_triangles.triangles)):
            self.triangles.append(Int3(
                pasted_triangles.triangles[i].x + num_vertices,
                pasted_triangles.triangles[i].y + num_vertices,
                pasted_triangles.triangles[i].z + num_vertices
            ))
