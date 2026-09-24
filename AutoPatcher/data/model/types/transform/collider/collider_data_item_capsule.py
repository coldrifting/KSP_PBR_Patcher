from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec3 import Vec3
from data.model.types.mu_tag import MuTag


class ColliderDataItemCapsule:
    def __init__(self, radius: float, height: float, direction: int, center: Vec3):
        self.radius = radius
        self.height = height
        self.direction = direction
        self.center = center

    def write(self, writer: ByteWriter, is_trigger: bool | None):
        if is_trigger is not None:
            writer.write_int(MuTag.CapsuleCollider2)
            writer.write_bool(is_trigger)
        else:
            writer.write_int(MuTag.CapsuleCollider)
        writer.write_float(self.radius)
        writer.write_float(self.height)
        writer.write_int(self.direction)
        writer.write_vec3(self.center)

    @staticmethod
    def read(reader: ByteReader) -> 'ColliderDataItemCapsule':
        radius = reader.read_float()
        height = reader.read_float()
        direction = reader.read_int()
        center = reader.read_vec3()

        return ColliderDataItemCapsule(
            radius = radius,
            height = height,
            direction = direction,
            center = center
        )
