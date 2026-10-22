from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec4 import Vec4
from data.model.types.tag.tag_mu import MuTag
from data.model.types.generic.mu_component import MuComponent


class Light(MuComponent):
    def __init__(self,
                 light_type: int,
                 intensity: float | int,
                 light_range: float | int,
                 color: Vec4,
                 culling_mask: int,
                 spot_angle: float | int):
        self.light_type: int = light_type
        self.intensity: float | int = intensity
        self.light_range: float | int = light_range
        self.color: Vec4 = color
        self.culling_mask: int = culling_mask
        self.spot_angle: float | int = spot_angle

    @staticmethod
    def read(reader: ByteReader) -> 'Light':
        light_type: int = reader.read_int()
        intensity: float | int = reader.read_float()
        light_range: float | int = reader.read_float()
        color: Vec4 = reader.read_vec4()
        culling_mask: int = reader.read_uint()
        spot_angle: float | int = reader.read_float()

        return Light(light_type=light_type,
                     intensity=intensity,
                     light_range=light_range,
                     color=color,
                     culling_mask=culling_mask,
                     spot_angle=spot_angle)

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.Light)

        writer.write_int(self.light_type)
        writer.write_float(self.intensity)
        writer.write_float(self.light_range)
        writer.write_vec4(self.color)
        writer.write_uint(self.culling_mask)
        writer.write_float(self.spot_angle)
