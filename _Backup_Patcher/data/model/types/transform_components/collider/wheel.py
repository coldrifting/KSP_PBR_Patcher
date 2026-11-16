from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec3 import Vec3
from data.model.types.generic.mu_component import MuComponent
from data.model.types.tag.tag_mu import MuTag
from data.model.types.transform_components.collider.wheel_components.friction import Friction
from data.model.types.transform_components.collider.wheel_components.spring import Spring


class ColliderWheel(MuComponent):
    def __init__(self,
                 mass: float,
                 radius: float,
                 suspension_distance: float,
                 center: Vec3,
                 suspension_spring: Spring,
                 forward_friction: Friction,
                 sideways_friction: Friction):
        self.mass = mass
        self.radius = radius
        self.suspension_distance = suspension_distance
        self.center = center
        self.suspension_spring = suspension_spring
        self.forward_friction = forward_friction
        self.sideways_friction = sideways_friction

    @staticmethod
    def read(reader: ByteReader) -> 'ColliderWheel':
        mass = reader.read_float()
        radius = reader.read_float()
        suspension_distance = reader.read_float()
        center = reader.read_vec3()

        suspension_spring = Spring().read(reader)
        forward_friction = Friction().read(reader)
        sideways_friction = Friction().read(reader)

        return ColliderWheel(
            mass=mass,
            radius=radius,
            suspension_distance=suspension_distance,
            center=center,
            suspension_spring=suspension_spring,
            forward_friction=forward_friction,
            sideways_friction=sideways_friction)

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.ColliderWheel)

        writer.write_float(self.mass)
        writer.write_float(self.radius)
        writer.write_float(self.suspension_distance)
        writer.write_vec3(self.center)

        self.suspension_spring.write(writer)
        self.forward_friction.write(writer)
        self.sideways_friction.write(writer)
