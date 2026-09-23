from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.color_byte import ColorByte
from data.model.types.core.int2 import Int2
from data.model.types.core.vec2 import Vec2
from data.model.types.core.vec3 import Vec3
from data.model.types.core.vec4 import Vec4
from data.model.types.core.int3 import Int3
from data.model.types.core.int4 import Int4
from data.model.types.mu_tag import MuTag


class MeshDataItem:
    def write(self, writer: ByteWriter):
        pass

    @staticmethod
    def read(reader: ByteReader, vertex_count: int) -> 'MeshDataItem':
        match reader.preview():
            case MuTag.MeshVertices:
                return MeshDataItemVertices.read_sub(reader, vertex_count)
            case MuTag.MeshUv:
                return MeshDataItemUvs.read_sub(reader, vertex_count)
            case MuTag.MeshUv2:
                return MeshDataItemUvs.read_sub(reader, vertex_count)
            case MuTag.MeshNormals:
                return MeshDataItemNormals.read_sub(reader, vertex_count)
            case MuTag.MeshTangents:
                return MeshDataItemTangents.read_sub(reader, vertex_count)
            case MuTag.MeshTriangles:
                return MeshDataItemTriangles.read_sub(reader)
            case MuTag.MeshBoneWeights:
                return MeshDataItemBoneWeights.read_sub(reader, vertex_count)
            case MuTag.MeshBindPoses:
                return MeshDataItemBindPoses.read_sub(reader)
            case MuTag.MeshVertexColors:
                return MeshDataItemVertexColors.read_sub(reader, vertex_count)

        raise Exception(f"Unknown tag with id: {reader.preview()}")

    def clone(self: 'MeshDataItem') -> 'MeshDataItem':
        match self:
            case MeshDataItemVertices():
                vertices = [x.clone() for x in self.vertices]
                return MeshDataItemVertices(vertices)
            case MeshDataItemUvs():
                uvs = [x.clone() for x in self.uvs]
                return MeshDataItemUvs(uvs, self.is_uv2)
            case MeshDataItemNormals():
                normals = [x.clone() for x in self.normals]
                return MeshDataItemNormals(normals)
            case MeshDataItemTangents():
                tangents = [x.clone() for x in self.tangents]
                return MeshDataItemTangents(tangents)
            case MeshDataItemTriangles():
                triangles = [x.clone() for x in self.triangles]
                return MeshDataItemTriangles(triangles)
            case MeshDataItemBoneWeights():
                bone_weights = [x for x in self.bone_weights]
                return MeshDataItemBoneWeights(bone_weights)
            case MeshDataItemBindPoses():
                poses = [x for x in self.poses]
                return MeshDataItemBindPoses(poses)
            case MeshDataItemVertexColors():
                vertex_colors = [x.clone() for x in self.vertex_colors]
                return MeshDataItemVertexColors(vertex_colors)

        raise Exception(f"Unknown class: {str(self)}")

    @staticmethod
    def merge(left: 'MeshDataItem', right: 'MeshDataItem', size: Int2) -> 'MeshDataItem':
        if isinstance(left, MeshDataItemUvs) and isinstance(right, MeshDataItemUvs):
            left.uvs.extend(right.uvs)
            return left
        elif isinstance(left, MeshDataItemUvs) and right is None:
            left.uvs.extend([Vec2(0,0) for _ in range(size.y)])
            return left
        elif left is None and isinstance(right, MeshDataItemUvs):
            right.uvs.extend([Vec2(0,0) for _ in range(size.x)])
            return right

        if isinstance(left, MeshDataItemNormals) and isinstance(right, MeshDataItemNormals):
            left.normals.extend(right.normals)
            return left
        elif isinstance(left, MeshDataItemNormals) and right is None:
            left.normals.extend([Vec3(0,0, 0) for _ in range(size.y)])
            return left
        elif left is None and isinstance(right, MeshDataItemNormals):
            right.normals.extend([Vec3(0,0, 0) for _ in range(size.x)])
            return right

        if isinstance(left, MeshDataItemTangents) and isinstance(right, MeshDataItemTangents):
            left.tangents.extend(right.tangents)
            return left
        elif isinstance(left, MeshDataItemTangents) and right is None:
            left.tangents.extend([Vec4(0,0, 0, 0) for _ in range(size.y)])
            return left
        elif left is None and isinstance(right, MeshDataItemTangents):
            right.tangents.extend([Vec4(0,0, 0, 0) for _ in range(size.x)])
            return right

        if isinstance(left, MeshDataItemVertexColors) and isinstance(right, MeshDataItemVertexColors):
            left.vertex_colors.extend(right.vertex_colors)
            return left
        elif isinstance(left, MeshDataItemVertexColors) and right is None:
            left.vertex_colors.extend([ColorByte(255,255, 255, 255) for _ in range(size.y)])
            return left
        elif left is None and isinstance(right, MeshDataItemVertexColors):
            right.vertex_colors.extend([ColorByte(255,255, 255, 255) for _ in range(size.x)])
            return right

        if isinstance(left, MeshDataItemBoneWeights) and isinstance(right, MeshDataItemBoneWeights):
            left.bone_weights.extend(right.bone_weights)
            return left
        elif isinstance(left, MeshDataItemBoneWeights) and right is None:
            left.bone_weights.extend([BoneWeight(Int4(0,0,0,0), Vec4(0,0,0,0)) for _ in range(size.y)])
            return left
        elif left is None and isinstance(right, MeshDataItemBoneWeights):
            right.bone_weights.extend([BoneWeight(Int4(0,0,0,0), Vec4(0,0,0,0)) for _ in range(size.x)])
            return right


        raise Exception(f"Unknown types: {type(left)}, {type(right)}")


class MeshDataItemBindPoses(MeshDataItem):
    def __init__(self, poses: list[int]):
        self.poses = poses

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshBindPoses)
        writer.write_int(len(self.poses) // 16)
        for pose in self.poses:
            writer.write_int(pose)

    @staticmethod
    def read_sub(reader: ByteReader) -> 'MeshDataItemBindPoses':
        reader.read_int()  # Consume Tag
        num_poses = reader.read_int() * 16

        poses = []
        for _ in range(num_poses):
            poses.append(reader.read_int())

        return MeshDataItemBindPoses(
            poses = poses
        )


class BoneWeight:
    def __init__(self, indices: Int4, weights: Vec4):
        self.indices = indices
        self.weights = weights


class MeshDataItemBoneWeights(MeshDataItem):
    def __init__(self, bone_weights: list[BoneWeight]):
        self.bone_weights = bone_weights

    def delete(self, indices: set[int]):
        for i in reversed(range(len(self.bone_weights))):
            if i in indices:
                del self.bone_weights[i]

    def paste(self, pasted_bone_weights: 'MeshDataItemBoneWeights'):
        for bone_weight in pasted_bone_weights.bone_weights:
            self.bone_weights.append(bone_weight)

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshBoneWeights)
        for bone_weight in self.bone_weights:
            writer.write_int4(bone_weight.indices)
            writer.write_vec4(bone_weight.weights)

    @staticmethod
    def read_sub(reader: ByteReader, vertex_count: int) -> 'MeshDataItemBoneWeights':
        reader.read_int()  # Consume Tag

        bone_weights = []
        for _ in range(vertex_count):
            bone_weight_indices = reader.read_int4()
            bone_weight_weights = reader.read_vec4()
            bone_weights.append(BoneWeight(bone_weight_indices, bone_weight_weights))

        return MeshDataItemBoneWeights(
            bone_weights = bone_weights
        )

class MeshDataItemNormals(MeshDataItem):
    def __init__(self, normals: list[Vec3]):
        self.normals = normals

    def __str__(self):
        return f"Normals: {len(self.normals)}"

    def delete(self, indices: set[int]):
        for i in reversed(range(len(self.normals))):
            if i in indices:
                del self.normals[i]

    def paste(self, pasted_normals: 'MeshDataItemNormals'):
        for normal in pasted_normals.normals:
            self.normals.append(normal)

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshNormals)
        for vertex in self.normals:
            writer.write_vec3(vertex)

    @staticmethod
    def read_sub(reader: ByteReader, vertex_count: int) -> 'MeshDataItemNormals':
        reader.read_int()  # Consume Tag

        normals = []
        for _ in range(vertex_count):
            normals.append(reader.read_vec3())

        return MeshDataItemNormals(
            normals = normals
        )


class MeshDataItemTangents(MeshDataItem):
    def __init__(self, tangents: list[Vec4]):
        self.tangents = tangents

    def __str__(self):
        return f"Tangents: {len(self.tangents)}"

    def delete(self, indices: set[int]):
        for i in reversed(range(len(self.tangents))):
            if i in indices:
                del self.tangents[i]

    def paste(self, pasted_tangents: 'MeshDataItemTangents'):
        for tangent in pasted_tangents.tangents:
            self.tangents.append(tangent)

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshTangents)
        for normal in self.tangents:
            writer.write_vec4(normal)

    @staticmethod
    def read_sub(reader: ByteReader, vertex_count: int) -> 'MeshDataItemTangents':
        reader.read_int()  # Consume Tag

        tangents = []
        for _ in range(vertex_count):
            tangents.append(reader.read_vec4())

        return MeshDataItemTangents(
            tangents = tangents
        )


class MeshDataItemTriangles(MeshDataItem):
    def __init__(self, triangles: list[Int3]):
        self.triangles = triangles

    def __str__(self):
        return f"Triangles: {len(self.triangles)}"

    def paste(self, pasted_triangles: 'MeshDataItemTriangles', num_vertices: int):
        for i in range(len(pasted_triangles.triangles)):
            self.triangles.append(Int3(
                pasted_triangles.triangles[i].x + num_vertices,
                pasted_triangles.triangles[i].y + num_vertices,
                pasted_triangles.triangles[i].z + num_vertices
            ))

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshTriangles)
        writer.write_int(len(self.triangles) * 3)
        for triangle in self.triangles:
            writer.write_int3(triangle)

    @staticmethod
    def read_sub(reader: ByteReader) -> 'MeshDataItemTriangles':
        reader.read_int()  # Consume Tag
        num_triangles = reader.read_int()

        triangles = []
        for _ in range(num_triangles // 3):
            triangles.append(reader.read_int3())

        return MeshDataItemTriangles(
            triangles = triangles
        )


class MeshDataItemUvs(MeshDataItem):
    def __init__(self, uvs: list[Vec2], is_uv2: bool = False):
        self.uvs = uvs
        self.is_uv2 = is_uv2

    def __str__(self):
        return f"Uv{'2' if self.is_uv2 else ''}s: {len(self.uvs)}"

    def delete(self, indices: set[int]):
        for i in reversed(range(len(self.uvs))):
            if i in indices:
                del self.uvs[i]

    def paste(self, pasted_uvs: 'MeshDataItemUvs'):
        for uv in pasted_uvs.uvs:
            self.uvs.append(uv)

    def write(self, writer: ByteWriter):
        if self.is_uv2:
            writer.write_int(MuTag.MeshUv2)
        else:
            writer.write_int(MuTag.MeshUv)

        for uv in self.uvs:
            writer.write_vec2(uv)

    @staticmethod
    def read_sub(reader: ByteReader, vertex_count: int) -> 'MeshDataItemUvs':
        is_uv2 = reader.read_int() == MuTag.MeshUv2

        uvs = []
        for _ in range(vertex_count):
            uvs.append(reader.read_vec2())

        return MeshDataItemUvs(
            uvs = uvs,
            is_uv2 = is_uv2
        )


class MeshDataItemVertexColors(MeshDataItem):
    def __init__(self, vertex_colors: list[ColorByte]):
        self.vertex_colors = vertex_colors

    def __str__(self):
        return f"Vertex Colors: {len(self.vertex_colors)}"

    def delete(self, indices: set[int]):
        for i in reversed(range(len(self.vertex_colors))):
            if i in indices:
                del self.vertex_colors[i]

    def paste(self, pasted_vertex_colors: 'MeshDataItemVertexColors'):
        for vertex_color in pasted_vertex_colors.vertex_colors:
            self.vertex_colors.append(vertex_color)

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshVertexColors)
        for vertex in self.vertex_colors:
            writer.write_color_byte(vertex)

    @staticmethod
    def read_sub(reader: ByteReader, vertex_count: int) -> 'MeshDataItemVertexColors':
        reader.read_int()  # Consume Tag

        vertex_colors = []
        for _ in range(vertex_count):
            vertex_colors.append(reader.read_color_byte())

        return MeshDataItemVertexColors(
            vertex_colors = vertex_colors
        )


class MeshDataItemVertices(MeshDataItem):
    def __init__(self, vertices: list[Vec3]):
        self.vertices = vertices

    def __str__(self):
        return f"Vertices: {len(self.vertices)}"

    def delete(self, indices: set[int]):
        for i in reversed(range(len(self.vertices))):
            if i in indices:
                del self.vertices[i]

    def paste(self, pasted_vertices: 'MeshDataItemVertices'):
        for vertex in pasted_vertices.vertices:
            self.vertices.append(vertex)

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshVertices)
        for vertex in self.vertices:
            writer.write_vec3(vertex)

    @staticmethod
    def read_sub(reader: ByteReader, vertex_count: int) -> 'MeshDataItemVertices':
        reader.read_int()  # Consume Tag

        vertices = []
        for _ in range(vertex_count):
            vertices.append(reader.read_vec3())

        return MeshDataItemVertices(
            vertices = vertices
        )