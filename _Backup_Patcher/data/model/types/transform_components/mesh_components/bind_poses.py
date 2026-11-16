from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.tag.tag_mu import MuTag
from data.model.types.transform_components.mesh_components.base import MuMeshComponent


class MeshBindPoses(MuMeshComponent):
    def __init__(self, poses: list[int]):
        self.poses: list[int] = poses

    @staticmethod
    def read(reader: ByteReader) -> 'MeshBindPoses':
        num_poses = reader.read_int()

        poses: list[int] = []
        for i in range(num_poses * 16):
            poses.append(reader.read_int())

        return MeshBindPoses(poses)

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshBindPoses)

        writer.write_int(len(self.poses) // 16)

        for pose in self.poses:
            writer.write_int(pose)
