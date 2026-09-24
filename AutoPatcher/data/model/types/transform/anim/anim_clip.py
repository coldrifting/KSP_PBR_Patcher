from data.model.types.transform.anim.anim_curve import AnimCurve
from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec3 import Vec3


class AnimClip:
    def __init__(self, clip_name: str, center: Vec3, size: Vec3, wrap_mode: int, curves: list[AnimCurve]):
        self.clip_name = clip_name
        self.center = center
        self.size = size
        self.wrap_mode = wrap_mode
        self.curves = curves

    def write(self, writer: ByteWriter):
        writer.write_str(self.clip_name)
        writer.write_vec3(self.center)
        writer.write_vec3(self.size)
        writer.write_int(self.wrap_mode)

        writer.write_int(len(self.curves))
        for curve in self.curves:
            curve.write(writer)

    @staticmethod
    def read(reader: ByteReader) -> 'AnimClip':
        clip_name = reader.read_str()
        center = reader.read_vec3()
        size = reader.read_vec3()
        wrap_mode = reader.read_int()

        curves = []
        num_curves = reader.read_int()
        for i in range(num_curves):
            curve = AnimCurve.read(reader)
            curves.append(curve)

        return AnimClip(
            clip_name = clip_name,
            center = center,
            size = size,
            wrap_mode = wrap_mode,
            curves = curves
        )