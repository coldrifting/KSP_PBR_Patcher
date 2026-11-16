from data.model.types.transform_components.animation_components.animation_key import AnimationKey
from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.int2 import Int2


class AnimationCurve:
    def __init__(self, curve_name: str = ""):
        self.curve_name = curve_name
        self.curve_property = ""
        self.curve_type = 0
        self.wrap_mode_in_out = Int2(0, 0)
        self.keys = []

    def read(self, reader: ByteReader) -> 'AnimationCurve':
        self.curve_name = reader.read_str()
        self.curve_property = reader.read_str()
        self.curve_type = reader.read_int()
        self.wrap_mode_in_out = reader.read_int2()

        self.keys = []
        num_keys = reader.read_int()
        for i in range(num_keys):
            key = AnimationKey().read(reader)
            self.keys.append(key)

        return self

    def write(self, writer: ByteWriter):
        writer.write_str(self.curve_name)
        writer.write_str(self.curve_property)
        writer.write_int(self.curve_type)
        writer.write_int2(self.wrap_mode_in_out)

        writer.write_int(len(self.keys))
        for key in self.keys:
            key.write(writer)
