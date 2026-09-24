from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec4 import Vec4
from data.model.types.mu_tag import MuTag


class LightData:
    def __init__(self, light_type: int, intensity: float, light_range: float, color: Vec4, culling_mask: int, spot_angle: float):
        self.light_type = light_type
        self.intensity = intensity
        self.light_range = light_range
        self.color = color
        self.culling_mask = culling_mask
        self.spot_angle = spot_angle

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.Light)
        writer.write_int(self.light_type)
        writer.write_float(self.intensity)
        writer.write_float(self.light_range)
        writer.write_vec4(self.color)
        writer.write_uint(self.culling_mask)
        writer.write_float(self.spot_angle)

    @staticmethod
    def read(reader: ByteReader) -> 'LightData':
        reader.read_int()  # Consume Tag
        light_type = reader.read_int()
        intensity = reader.read_float()
        light_range = reader.read_float()
        color = reader.read_vec4()
        culling_mask = reader.read_uint()
        spot_angle = reader.read_float()

        return LightData(
            light_type = light_type,
            intensity = intensity,
            light_range = light_range,
            color = color,
            culling_mask = culling_mask,
            spot_angle = spot_angle
        )