from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.color_byte import ColorByte
from data.model.types.core.int3 import Int3
from data.model.types.core.vec2 import Vec2
from data.model.types.core.vec3 import Vec3
from data.model.types.core.vec4 import Vec4
from data.model.types.generic.mu_component import MuComponent
from data.model.types.tag.tag_mu import MuTag
from data.model.types.transform_components.mesh_components.base import MuMeshComponent
from data.model.types.transform_components.mesh_components.bind_poses import MeshBindPoses
from data.model.types.transform_components.mesh_components.bone_weights import MeshBoneWeights, BoneWeight
from data.model.types.transform_components.mesh_components.normals import MeshNormals
from data.model.types.transform_components.mesh_components.tangents import MeshTangents
from data.model.types.transform_components.mesh_components.triangles import MeshTriangles
from data.model.types.transform_components.mesh_components.uvs import MeshUvs
from data.model.types.transform_components.mesh_components.vertex_colors import MeshVertexColors
from data.model.types.transform_components.mesh_components.vertex_data import VertexData
from data.model.types.transform_components.mesh_components.vertices import MeshVertices

class Mesh(MuComponent):
    def __init__(self,
                 num_submeshes: int,
                 ordering: list[MuTag],
                 vertex_data: list[VertexData],
                 triangles: list[Int3],
                 bind_poses: MeshBindPoses | None,
                 has_filter: bool = True):
        self.num_submeshes: int = num_submeshes
        self.ordering: list[MuTag] = ordering
        self.vertex_data: list[VertexData] = vertex_data
        self.triangles: list[Int3] = triangles
        self.bind_poses: MeshBindPoses | None = bind_poses
        self.has_filter: bool = has_filter

    @staticmethod
    def read(reader: ByteReader) -> 'Mesh':
        tag = reader.read_tag()
        if tag != MuTag.MeshStart:
            raise ValueError(f"Invalid tag {tag}")

        num_vertices = reader.read_int()
        num_submeshes = reader.read_int()

        data: dict[MuTag, MuMeshComponent] = {}

        while True:
            tag = reader.read_tag()
            match tag:
                case MuTag.MeshVertices:
                    data[tag] = MeshVertices.read(reader, num_vertices)
                case MuTag.MeshUv:
                    data[tag] = MeshUvs.read(reader, num_vertices, False)
                case MuTag.MeshUv2:
                    data[tag] = MeshUvs.read(reader, num_vertices, True)
                case MuTag.MeshNormals:
                    data[tag] = MeshNormals.read(reader, num_vertices)
                case MuTag.MeshTangents:
                    data[tag] = MeshTangents.read(reader, num_vertices)
                case MuTag.MeshBoneWeights:
                    data[tag] = MeshBoneWeights.read(reader, num_vertices)
                case MuTag.MeshVertexColors:
                    data[tag] = MeshVertexColors.read(reader, num_vertices)
                case MuTag.MeshTriangles:
                    data[tag] = MeshTriangles.read(reader)
                case MuTag.MeshBindPoses:
                    data[tag] = MeshBindPoses.read(reader)
                case MuTag.MeshEnd:
                    break
                case _:
                    raise ValueError(f"Invalid tag {tag}")

        # Pack related vertex data into single data structure
        ordering = list(data.keys())

        vertices = data.get(MuTag.MeshVertices, None)
        if not isinstance(vertices, MeshVertices):
            raise

        vertex_data: list[VertexData] = []

        bind_poses = data.get(MuTag.MeshBindPoses, None)
        if bind_poses is not None and not isinstance(bind_poses, MeshBindPoses):
            raise

        for i in range(0, num_vertices):
            vertex_data.append(VertexData(position=vertices.vertices[i]))

            for tag in ordering:
                item = data[tag]
                match item:
                    case MeshBindPoses():
                        continue
                    case MeshVertices():
                        continue
                    case MeshTriangles():
                        continue
                    case MeshUvs():
                        if item.is_uv2:
                            vertex_data[i].uv2 = item.uvs[i]
                        else:
                            vertex_data[i].uv = item.uvs[i]
                    case MeshNormals():
                        vertex_data[i].normal = item.normals[i]
                    case MeshTangents():
                        vertex_data[i].tangent = item.tangents[i]
                    case MeshVertexColors():
                        vertex_data[i].vertex_color = item.vertex_colors[i]
                    case MeshBoneWeights():
                        vertex_data[i].bone_weight = item.bone_weights[i]
                    case _:
                        raise NotImplementedError()

        triangles = data[MuTag.MeshTriangles]
        if not isinstance(triangles, MeshTriangles):
            raise

        return Mesh(num_submeshes, ordering, vertex_data, triangles.triangles, bind_poses)

    def write(self, writer: ByteWriter):
        if self.has_filter:
            writer.write_tag(MuTag.MeshFilter)

        writer.write_tag(MuTag.MeshStart)

        writer.write_int(len(self.vertex_data))
        writer.write_int(self.num_submeshes)

        data: dict[MuTag, MuMeshComponent] = {}

        verts: list[Vec3] = []
        uvs: list[Vec2] = []
        uv2s: list[Vec2] = []
        normals: list[Vec3] = []
        tangents: list[Vec4] = []
        vertex_colors: list[ColorByte] = []
        bone_weights: list[BoneWeight] = []

        for vertex in self.vertex_data:
            verts.append(vertex.position)

            if vertex.uv is not None:
                uvs.append(vertex.uv)

            if vertex.uv2 is not None:
                uv2s.append(vertex.uv2)

            if vertex.normal is not None:
                normals.append(vertex.normal)

            if vertex.tangent is not None:
                tangents.append(vertex.tangent)

            if vertex.vertex_color is not None:
                vertex_colors.append(vertex.vertex_color)

            if vertex.bone_weight is not None:
                bone_weights.append(vertex.bone_weight)

        for tag in self.ordering:
            match tag:
                case MuTag.MeshVertices:
                    data[tag] = MeshVertices(vertices=verts)
                case MuTag.MeshUv:
                    data[tag] = MeshUvs(uvs=uvs, is_uv2=False)
                case MuTag.MeshUv2:
                    data[tag] = MeshUvs(uvs=uv2s, is_uv2=True)
                case MuTag.MeshNormals:
                    data[tag] = MeshNormals(normals=normals)
                case MuTag.MeshTangents:
                    data[tag] = MeshTangents(tangents=tangents)
                case MuTag.MeshVertexColors:
                    data[tag] = MeshVertexColors(vertex_colors=vertex_colors)
                case MuTag.MeshBoneWeights:
                    data[tag] = MeshBoneWeights(bone_weights=bone_weights)
                case MuTag.MeshBindPoses:
                    if self.bind_poses is not None:
                        data[tag] = self.bind_poses
                case MuTag.MeshTriangles:
                    data[tag] = MeshTriangles(triangles=self.triangles)

        for data_item in data.values():
            data_item.write(writer)

        writer.write_tag(MuTag.MeshEnd)
