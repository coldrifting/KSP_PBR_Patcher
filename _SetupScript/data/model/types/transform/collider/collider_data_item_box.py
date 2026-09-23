from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec3 import Vec3
from data.model.types.mu_tag import MuTag


class ColliderDataItemBox:
    def __init__(self, size: Vec3, center: Vec3):
        self.size = size
        self.center = center

    def write(self, writer: ByteWriter, is_trigger: bool | None):
        if is_trigger is not None:
            writer.write_int(MuTag.BoxCollider2)
            writer.write_bool(is_trigger)
        else:
            writer.write_int(MuTag.BoxCollider)
        writer.write_vec3(self.size)
        writer.write_vec3(self.center)

    @staticmethod
    def read(reader: ByteReader) -> 'ColliderDataItemBox':
        size = reader.read_vec3()
        center = reader.read_vec3()

        return ColliderDataItemBox(
            size = size,
            center = center
        )