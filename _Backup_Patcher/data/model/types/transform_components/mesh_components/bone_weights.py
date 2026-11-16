from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.int4 import Int4
from data.model.types.core.vec4 import Vec4
from data.model.types.tag.tag_mu import MuTag
from data.model.types.transform_components.mesh_components.base import MuMeshComponent


class BoneWeight:
    def __init__(self, indices: Int4, weights: Vec4):
        self.indices = indices
        self.weights = weights


class MeshBoneWeights(MuMeshComponent):
    def __init__(self, bone_weights: list[BoneWeight]):
        self.bone_weights = bone_weights

    @staticmethod
    def read(reader: ByteReader, num_vertices: int) -> 'MeshBoneWeights':
        bone_weights: list[BoneWeight] = []

        for _ in range(num_vertices):
            bone_weight_indices = reader.read_int4()
            bone_weight_weights = reader.read_vec4()
            bone_weights.append(BoneWeight(bone_weight_indices, bone_weight_weights))

        return MeshBoneWeights(bone_weights=bone_weights)

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshBoneWeights)

        for bone_weight in self.bone_weights:
            writer.write_int4(bone_weight.indices)
            writer.write_vec4(bone_weight.weights)

    # Modifications
    def delete(self, indices: set[int]):
        for i in reversed(range(len(self.bone_weights))):
            if i in indices:
                del self.bone_weights[i]

    def paste(self, pasted_bone_weights: 'MeshBoneWeights'):
        for bone_weight in pasted_bone_weights.bone_weights:
            self.bone_weights.append(bone_weight)
