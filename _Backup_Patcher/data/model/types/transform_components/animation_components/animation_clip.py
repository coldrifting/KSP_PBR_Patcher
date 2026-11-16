from data.model.types.transform_components.animation_components.animation_curve import AnimationCurve
from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec3 import Vec3


class AnimationClip:
    def __init__(self, clip_name: str = ""):
        self.clip_name = clip_name
        self.center = Vec3(0, 0, 0)
        self.size = Vec3(1, 1, 1)
        self.wrap_mode = 0
        self.curves = []

    def read(self, reader: ByteReader) -> 'AnimationClip':
        self.clip_name = reader.read_str()
        self.center = reader.read_vec3()
        self.size = reader.read_vec3()
        self.wrap_mode = reader.read_int()

        self.curves = []
        num_curves = reader.read_int()
        for i in range(num_curves):
            curve = AnimationCurve().read(reader)
            self.curves.append(curve)

        return self

    def write(self, writer: ByteWriter):
        writer.write_str(self.clip_name)
        writer.write_vec3(self.center)
        writer.write_vec3(self.size)
        writer.write_int(self.wrap_mode)

        writer.write_int(len(self.curves))
        for curve in self.curves:
            curve.write(writer)
