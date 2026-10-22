from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec3 import Vec3
from data.model.types.generic.mu_component_collider import MuComponentCollider
from data.model.types.tag.tag_mu import MuTag


class ColliderSphere(MuComponentCollider):
    def __init__(self, is_trigger: bool | None, radius: float | int, center: Vec3):
        self.is_trigger = is_trigger
        self.radius = radius
        self.center = center

    @staticmethod
    def read(reader: ByteReader, has_trigger: bool | None = None) -> 'ColliderSphere':
        if has_trigger:
            is_trigger = reader.read_bool()
        else:
            is_trigger = None

        radius = reader.read_float()
        center = reader.read_vec3()

        return ColliderSphere(is_trigger, radius, center)

    def write(self, writer: ByteWriter):
        if self.is_trigger is not None:
            writer.write_int(MuTag.ColliderSphere2)
            writer.write_bool(self.is_trigger)
        else:
            writer.write_int(MuTag.ColliderSphere)

        writer.write_float(self.radius)
        writer.write_vec3(self.center)
