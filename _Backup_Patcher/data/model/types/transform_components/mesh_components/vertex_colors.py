from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.color_byte import ColorByte
from data.model.types.tag.tag_mu import MuTag
from data.model.types.transform_components.mesh_components.base import MuMeshComponent


class MeshVertexColors(MuMeshComponent):
    def __init__(self, vertex_colors: list[ColorByte]):
        self.vertex_colors: list[ColorByte] = vertex_colors

    def __str__(self):
        return f"Vertex Colors: {len(self.vertex_colors)}"

    @staticmethod
    def read(reader: ByteReader, num_vertices: int) -> 'MeshVertexColors':
        vertex_colors: list[ColorByte] = []

        for i in range(num_vertices):
            vertex_colors.append(reader.read_color_byte())

        return MeshVertexColors(vertex_colors=vertex_colors)

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshVertexColors)

        for vertex in self.vertex_colors:
            writer.write_color_byte(vertex)

    # Modifications
    def delete(self, indices: set[int]):
        for i in reversed(range(len(self.vertex_colors))):
            if i in indices:
                del self.vertex_colors[i]

    def paste(self, pasted_vertex_colors: 'MeshVertexColors'):
        for vertex_color in pasted_vertex_colors.vertex_colors:
            self.vertex_colors.append(vertex_color)
