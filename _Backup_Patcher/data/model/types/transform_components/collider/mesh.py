from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.generic.mu_component_collider import MuComponentCollider
from data.model.types.tag.tag_mu import MuTag
from data.model.types.transform_components.mesh import Mesh


class ColliderMesh(MuComponentCollider):
    def __init__(self, is_trigger: bool | None, is_convex: bool, mesh_data: Mesh):
        self.is_trigger = is_trigger
        self.is_convex = is_convex
        self.mesh_data = mesh_data

    @staticmethod
    def read(reader: ByteReader, has_trigger: bool = False) -> 'ColliderMesh':
        if has_trigger:
            is_trigger = reader.read_bool()
        else:
            is_trigger = None

        is_convex = reader.read_bool()
        mesh_data = Mesh.read(reader)
        mesh_data.has_filter = False

        return ColliderMesh(is_trigger, is_convex, mesh_data)

    def write(self, writer: ByteWriter):
        if self.is_trigger is not None:
            writer.write_int(MuTag.ColliderMesh2)
            writer.write_bool(self.is_trigger)
        else:
            writer.write_int(MuTag.ColliderMesh)

        writer.write_bool(self.is_convex)

        if self.mesh_data is not None:
            self.mesh_data.write(writer)
