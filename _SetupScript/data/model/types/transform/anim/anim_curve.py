from data.model.types.transform.anim.anim_key import AnimKey
from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.int2 import Int2


class AnimCurve:
    def __init__(self, curve_name: str, curve_property: str, curve_type: int, wrap_mode_in_out: Int2, keys: list[AnimKey]):
        self.curve_name = curve_name
        self.curve_property = curve_property
        self.curve_type = curve_type
        self.wrap_mode_in_out = wrap_mode_in_out
        self.keys = keys

    def write(self, writer: ByteWriter):
        writer.write_str(self.curve_name)
        writer.write_str(self.curve_property)
        writer.write_int(self.curve_type)
        writer.write_int2(self.wrap_mode_in_out)

        writer.write_int(len(self.keys))
        for key in self.keys:
            key.write(writer)

    @staticmethod
    def read(reader: ByteReader) -> 'AnimCurve':
        curve_name = reader.read_str()
        curve_property = reader.read_str()
        curve_type = reader.read_int()
        wrap_mode_in_out = reader.read_int2()

        keys = []
        num_keys = reader.read_int()
        for i in range(num_keys):
            key = AnimKey.read(reader)
            keys.append(key)

        return AnimCurve(
            curve_name = curve_name,
            curve_property = curve_property,
            curve_type = curve_type,
            wrap_mode_in_out = wrap_mode_in_out,
            keys = keys
        )