from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec3 import Vec3
from data.model.types.generic.mu_component_collider import MuComponentCollider
from data.model.types.tag.tag_mu import MuTag


class ColliderCapsule(MuComponentCollider):
    def __init__(self,
                 is_trigger: bool | None,
                 radius: float | int,
                 height: float | int,
                 direction: int,
                 center: Vec3):
        self.is_trigger = is_trigger
        self.radius = radius
        self.height = height
        self.direction = direction
        self.center = center

    @staticmethod
    def read(reader: ByteReader, has_trigger: bool = False) -> 'ColliderCapsule':
        if has_trigger:
            is_trigger = reader.read_bool()
        else:
            is_trigger = None

        radius = reader.read_float()
        height = reader.read_float()
        direction = reader.read_int()
        center = reader.read_vec3()

        return ColliderCapsule(is_trigger, radius, height, direction, center)

    def write(self, writer: ByteWriter):
        if self.is_trigger is not None:
            writer.write_int(MuTag.ColliderCapsule2)
            writer.write_bool(self.is_trigger)
        else:
            writer.write_int(MuTag.ColliderCapsule)

        writer.write_float(self.radius)
        writer.write_float(self.height)
        writer.write_int(self.direction)
        writer.write_vec3(self.center)
