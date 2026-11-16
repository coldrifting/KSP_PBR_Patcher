from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec2 import Vec2
from data.model.types.core.vec3 import Vec3
from data.model.types.core.vec4 import Vec4
from data.model.types.generic.mu_component import MuComponent
from data.model.types.tag.tag_mu import MuTag


class Particles(MuComponent):
    def __init__(self,
                 emit: bool,
                 shape: int,
                 shape3d: Vec3,
                 shape2d: Vec2,
                 shape1d: float | int,
                 color: Vec4,
                 use_world_space: bool,
                 size_min_max: Vec2,
                 energy_min_max: Vec2,
                 emission_min_max: Vec2,
                 velocity_world: Vec3,
                 velocity_local: Vec3,
                 velocity_random: Vec3,
                 velocity_emit_scale: float | int,
                 velocity_angular: float | int,
                 velocity_angular_random: float | int,
                 rotation_random: bool,
                 animate_color: bool,
                 color_animations: list[Vec4],
                 axis_rotation_world: Vec3,
                 axis_rotation_local: Vec3,
                 size_grow: float | int,
                 force_random: Vec3,
                 force: Vec3,
                 damping: float | int,
                 shadow_cast: bool,
                 shadow_receive: bool,
                 scale_length: float | int,
                 scale_velocity: float | int,
                 max_particle_size: float | int,
                 particle_render_mode: int,
                 uv_animation: Vec3,
                 count: int):
        self.emit: bool = emit
        self.shape: int = shape
        self.shape3d: Vec3 = shape3d
        self.shape2d: Vec2 = shape2d
        self.shape1d: float | int = shape1d
        self.color: Vec4 = color
        self.use_world_space: bool = use_world_space
        self.size_min_max: Vec2 = size_min_max
        self.energy_min_max: Vec2 = energy_min_max
        self.emission_min_max: Vec2 = emission_min_max
        self.velocity_world: Vec3 = velocity_world
        self.velocity_local: Vec3 = velocity_local
        self.velocity_random: Vec3 = velocity_random
        self.velocity_emit_scale: float | int = velocity_emit_scale
        self.velocity_angular: float | int = velocity_angular
        self.velocity_angular_random: float | int = velocity_angular_random
        self.rotation_random: bool = rotation_random
        self.animate_color: bool = animate_color
        self.color_animations: list[Vec4] = color_animations
        self.axis_rotation_world: Vec3 = axis_rotation_world
        self.axis_rotation_local: Vec3 = axis_rotation_local
        self.size_grow: float | int = size_grow
        self.force_random: Vec3 = force_random
        self.force: Vec3 = force
        self.damping: float | int = damping
        self.shadow_cast: bool = shadow_cast
        self.shadow_receive: bool = shadow_receive
        self.scale_length: float | int = scale_length
        self.scale_velocity: float | int = scale_velocity
        self.max_particle_size: float | int = max_particle_size
        self.particle_render_mode: int = particle_render_mode
        self.uv_animation: Vec3 = uv_animation  # xtile, ytile, cycles
        self.count: int = count

    @staticmethod
    def read(reader: ByteReader) -> 'Particles':
        emit: bool = reader.read_bool()
        shape: int = reader.read_int()
        shape3d: Vec3 = reader.read_vec3()
        shape2d: Vec2 = reader.read_vec2()
        shape1d: float | int = reader.read_float()
        color: Vec4 = reader.read_vec4()
        use_world_space: bool = reader.read_bool()
        size_min_max: Vec2 = reader.read_vec2()
        energy_min_max: Vec2 = reader.read_vec2()
        emission_min_max: Vec2 = reader.read_vec2()
        velocity_world: Vec3 = reader.read_vec3()
        velocity_local: Vec3 = reader.read_vec3()
        velocity_random: Vec3 = reader.read_vec3()
        velocity_emit_scale: float | int = reader.read_float()
        velocity_angular: float | int = reader.read_float()
        velocity_angular_random: float | int = reader.read_float()
        rotation_random: bool = reader.read_bool()
        animate_color: bool = reader.read_bool()
        color_animations: list[Vec4] = []
        for i in range(5):
            color_animations.append(reader.read_vec4())
        axis_rotation_world: Vec3 = reader.read_vec3()
        axis_rotation_local: Vec3 = reader.read_vec3()
        size_grow: float | int = reader.read_float()
        force_random: Vec3 = reader.read_vec3()
        force: Vec3 = reader.read_vec3()
        damping: float | int = reader.read_float()
        shadow_cast: bool = reader.read_bool()
        shadow_receive: bool = reader.read_bool()
        scale_length: float | int = reader.read_float()
        scale_velocity: float | int = reader.read_float()
        max_particle_size: float | int = reader.read_float()
        particle_render_mode: int = reader.read_int()
        uv_animation: Vec3 = reader.read_vec3()
        count: int = reader.read_int()

        return Particles(
            emit=emit,
            shape=shape,
            shape3d=shape3d,
            shape2d=shape2d,
            shape1d=shape1d,
            color=color,
            use_world_space=use_world_space,
            size_min_max=size_min_max,
            energy_min_max=energy_min_max,
            emission_min_max=emission_min_max,
            velocity_world=velocity_world,
            velocity_local=velocity_local,
            velocity_random=velocity_random,
            velocity_emit_scale=velocity_emit_scale,
            velocity_angular=velocity_angular,
            velocity_angular_random=velocity_angular_random,
            rotation_random=rotation_random,
            animate_color=animate_color,
            color_animations=color_animations,
            axis_rotation_world=axis_rotation_world,
            axis_rotation_local=axis_rotation_local,
            size_grow=size_grow,
            force_random=force_random,
            force=force,
            damping=damping,
            shadow_cast=shadow_cast,
            shadow_receive=shadow_receive,
            scale_length=scale_length,
            scale_velocity=scale_velocity,
            max_particle_size=max_particle_size,
            particle_render_mode=particle_render_mode,
            uv_animation=uv_animation,
            count=count,
        )

    def write(self, writer: ByteWriter):
        writer.write_tag(MuTag.Particles)

        writer.write_bool(self.emit)
        writer.write_int(self.shape)
        writer.write_vec3(self.shape3d)
        writer.write_vec2(self.shape2d)
        writer.write_float(self.shape1d)
        writer.write_vec4(self.color)
        writer.write_bool(self.use_world_space)
        writer.write_vec2(self.size_min_max)
        writer.write_vec2(self.energy_min_max)
        writer.write_vec2(self.emission_min_max)
        writer.write_vec3(self.velocity_world)
        writer.write_vec3(self.velocity_local)
        writer.write_vec3(self.velocity_random)
        writer.write_float(self.velocity_emit_scale)
        writer.write_float(self.velocity_angular)
        writer.write_float(self.velocity_angular_random)
        writer.write_bool(self.rotation_random)
        writer.write_bool(self.animate_color)

        for i in range(5):
            writer.write_vec4(self.color_animations[i])

        writer.write_vec3(self.axis_rotation_world)
        writer.write_vec3(self.axis_rotation_local)
        writer.write_float(self.size_grow)
        writer.write_vec3(self.force_random)
        writer.write_vec3(self.force)
        writer.write_float(self.damping)
        writer.write_bool(self.shadow_cast)
        writer.write_bool(self.shadow_receive)
        writer.write_float(self.scale_length)
        writer.write_float(self.scale_velocity)
        writer.write_float(self.max_particle_size)
        writer.write_int(self.particle_render_mode)
        writer.write_vec3(self.uv_animation)
        writer.write_int(self.count)
