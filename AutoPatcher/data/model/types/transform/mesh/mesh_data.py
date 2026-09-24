from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.int2 import Int2
from data.model.types.core.int3 import Int3
from data.model.types.core.vec2 import Vec2
from data.model.types.core.vec3 import Vec3
from data.model.types.transform.mesh.mesh_data_item import MeshDataItem, MeshDataItemVertices, MeshDataItemUvs, \
    MeshDataItemNormals, MeshDataItemTangents, MeshDataItemTriangles, MeshDataItemBoneWeights, MeshDataItemBindPoses, \
    MeshDataItemVertexColors
from data.model.types.transform.mesh.mesh_renderer_settings import MeshRendererSettings
from data.model.types.mu_tag import MuTag
from utils.exceptions import ArgumentException


class MeshData:
    def __init__(self,
                 vertex_count: int,
                 submesh_count: int,
                 items: dict[MuTag, MeshDataItem] | None = None,
                 render_settings: MeshRendererSettings | None = None):
        self.vertex_count = vertex_count
        self.submesh_count = submesh_count

        # Preserver tag order
        self.items = items if items is not None else {}

        self.render_settings: MeshRendererSettings | None = render_settings

    def __str__(self) -> str:
        return f"Mesh Data (Vertices: {self.vertex_count})"

    def vertices(self) -> list[Vec3]:
        item = self.items.get(MuTag.MeshVertices, None)
        if isinstance(item, MeshDataItemVertices):
            return item.vertices

        raise AttributeError("No vertices found for mesh")

    def triangles(self) -> list[Int3]:
        item = self.items.get(MuTag.MeshTriangles, None)
        if isinstance(item, MeshDataItemTriangles):
            return item.triangles

        raise AttributeError("No triangles found for mesh")

    def uvs(self) -> list[Vec2]:
        item = self.items.get(MuTag.MeshUv, None)
        if isinstance(item, MeshDataItemUvs):
            return item.uvs

        raise AttributeError(f"No uvs found for mesh")

    def normals(self) -> list[Vec3]:
        item = self.items.get(MuTag.MeshNormals, None)
        if isinstance(item, MeshDataItemNormals):
            return item.normals

        raise AttributeError(f"No normals found for mesh")

    def clone(self, clear: bool = False) -> 'MeshData':
        items_new: dict[MuTag, MeshDataItem] = {}
        for item in self.items.values():
            item_new = item.clone()
            match item_new:
                case MeshDataItemVertices():
                    items_new[MuTag.MeshVertices] = MeshDataItemVertices([]) if clear else item_new
                case MeshDataItemUvs():
                    uvs = MeshDataItemUvs([], item_new.is_uv2) if clear else item_new
                    if item_new.is_uv2:
                        items_new[MuTag.MeshUv2] = uvs
                    else:
                        items_new[MuTag.MeshUv] = uvs
                case MeshDataItemNormals():
                    items_new[MuTag.MeshNormals] = MeshDataItemNormals([]) if clear else item_new
                case MeshDataItemTangents():
                    items_new[MuTag.MeshTangents] = MeshDataItemTangents([]) if clear else item_new
                case MeshDataItemTriangles():
                    items_new[MuTag.MeshTriangles] = MeshDataItemTriangles([]) if clear else item_new
                case MeshDataItemBoneWeights():
                    items_new[MuTag.MeshBoneWeights] = MeshDataItemBoneWeights([]) if clear else item_new
                case MeshDataItemBindPoses():
                    items_new[MuTag.MeshBindPoses] = MeshDataItemBindPoses([]) if clear else item_new
                case MeshDataItemVertexColors():
                    items_new[MuTag.MeshVertexColors] = MeshDataItemVertexColors([]) if clear else item_new

        return MeshData(
            0 if clear else self.vertex_count,
            1 if clear else self.submesh_count,
            items_new,
            None if self.render_settings is None else self.render_settings.clone())

    def merge(self, other: 'MeshData'):
        self_keys = set(self.items.keys())
        other_keys = set(other.items.keys())

        all_keys = self_keys.union(other_keys)
        all_keys.remove(MuTag.MeshVertices)
        all_keys.remove(MuTag.MeshTriangles)

        for key in all_keys:
            self_item = self.items.get(key, None)
            other_item = other.items.get(key, None)
            if self_item is None and other_item is None:
                continue

            self.items[key] = MeshDataItem.merge(self_item, other_item, Int2(self.vertex_count, other.vertex_count))

        self_vertices = self.items[MuTag.MeshVertices]
        if not isinstance(self_vertices, MeshDataItemVertices):
            raise ArgumentException("Wrong type of object in MeshVertices Tag")

        other_vertices = other.items[MuTag.MeshVertices]
        if not isinstance(other_vertices, MeshDataItemVertices):
            raise ArgumentException("Wrong type of object in MeshVertices Tag")

        for vertex in other_vertices.vertices:
            self_vertices.vertices.append(vertex)

        self_triangles = self.items[MuTag.MeshTriangles]
        other_triangles = other.items[MuTag.MeshTriangles]
        if isinstance(self_triangles, MeshDataItemTriangles) and isinstance(other_triangles, MeshDataItemTriangles):
            for triangle in other_triangles.triangles:
                triangle_updated = Int3(
                    triangle.x + len(self_vertices.vertices) - len(other_vertices.vertices),
                    triangle.y + len(self_vertices.vertices) - len(other_vertices.vertices),
                    triangle.z + len(self_vertices.vertices) - len(other_vertices.vertices),
                )
                self_triangles.triangles.append(triangle_updated)

        self.vertex_count += other.vertex_count

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshStart)
        writer.write_int(self.vertex_count)
        writer.write_int(self.submesh_count)

        for item in self.items.values():
            item.write(writer)

        writer.write_int(MuTag.MeshEnd)

        if self.render_settings is not None:
            self.render_settings.write(writer)

    @staticmethod
    def read(reader: ByteReader) -> 'MeshData':
        reader.read_int()  # Consume MeshStart Tag
        vertex_count = reader.read_int()
        submesh_count = reader.read_int()

        items = {}
        while reader.preview() != MuTag.MeshEnd:
            tag = reader.preview()
            item = MeshDataItem.read(reader, vertex_count)
            items[tag] = item

        reader.read_int()  # Consume MeshEnd Tag
        render_settings = MeshRendererSettings.read(reader) if reader.preview() == MuTag.MeshRenderer else None

        return MeshData(
            vertex_count = vertex_count,
            submesh_count = submesh_count,
            items = items,
            render_settings = render_settings
        )