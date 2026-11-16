from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec3 import Vec3
from data.model.types.generic.mu_component_collider import MuComponentCollider
from data.model.types.tag.tag_mu import MuTag


class ColliderBox(MuComponentCollider):
    def __init__(self,
                 is_trigger: bool | None,
                 size: Vec3,
                 center: Vec3):
        self.is_trigger: bool | None = is_trigger
        self.size: Vec3 = size
        self.center: Vec3 = center

    @staticmethod
    def read(reader: ByteReader, has_trigger: bool = False) -> 'ColliderBox':
        if has_trigger:
            is_trigger = reader.read_bool()
        else:
            is_trigger = None

        size = reader.read_vec3()
        center = reader.read_vec3()

        return ColliderBox(is_trigger, size, center)

    def write(self, writer: ByteWriter):
        if self.is_trigger is not None:
            writer.write_int(MuTag.ColliderBox2)
            writer.write_bool(self.is_trigger)
        else:
            writer.write_int(MuTag.ColliderBox)

        writer.write_vec3(self.size)
        writer.write_vec3(self.center)
