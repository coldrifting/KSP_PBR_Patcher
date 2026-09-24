from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.transform.mesh.mesh_data import MeshData
from data.model.types.mu_tag import MuTag


class ColliderDataItemMesh:
    def __init__(self, is_convex: bool, mesh_data: MeshData):
        self.is_convex = is_convex
        self.mesh_data = mesh_data

    def write(self, writer: ByteWriter, is_trigger: bool | None):
        if is_trigger is not None:
            writer.write_int(MuTag.MeshCollider2)
            writer.write_bool(is_trigger)
        else:
            writer.write_int(MuTag.MeshCollider)
        writer.write_bool(self.is_convex)
        self.mesh_data.write(writer)

    @staticmethod
    def read(reader: ByteReader) -> 'ColliderDataItemMesh':
        is_convex = reader.read_bool()
        mesh_data = MeshData.read(reader)

        return ColliderDataItemMesh(
            is_convex = is_convex,
            mesh_data = mesh_data
        )