from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec3 import Vec3
from data.model.types.transform.mesh.mesh_data import MeshData
from data.model.types.mu_tag import MuTag


class SkinnedMeshData:
    def __init__(self, material_indices: list[int], center: Vec3, size: Vec3, quality: int, update_when_offscreen: bool, bone_names: list[str], mesh_data: MeshData):
        self.material_indices = material_indices
        self.center = center
        self.size = size
        self.quality = quality
        self.update_when_offscreen = update_when_offscreen
        self.bone_names = bone_names
        self.mesh_data = mesh_data

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.SkinnedMeshRenderer)

        writer.write_int(len(self.material_indices))
        for material_index in self.material_indices:
            writer.write_int(material_index)

        writer.write_vec3(self.center)
        writer.write_vec3(self.size)
        writer.write_int(self.quality)
        writer.write_bool(self.update_when_offscreen)

        writer.write_int(len(self.bone_names))
        for bone_name in self.bone_names:
            writer.write_str(bone_name)

        self.mesh_data.write(writer)

    @staticmethod
    def read(reader: ByteReader) -> 'SkinnedMeshData':
        reader.read_int()  # Consume Tag

        material_indices = []
        for material_index in range(reader.read_int()):
            material_indices.append(reader.read_int())

        center = reader.read_vec3()
        size = reader.read_vec3()
        quality = reader.read_int()
        update_when_offscreen = reader.read_bool()

        bone_names = []
        for _ in range(reader.read_int()):
            bone_names.append(reader.read_str())

        mesh_data = MeshData.read(reader)

        return SkinnedMeshData(
            material_indices = material_indices,
            center = center,
            size = size,
            quality = quality,
            update_when_offscreen = update_when_offscreen,
            bone_names = bone_names,
            mesh_data = mesh_data
        )