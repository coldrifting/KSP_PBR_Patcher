from data.model.types.core.color_byte import ColorByte
from data.model.types.core.vec2 import Vec2
from data.model.types.core.vec3 import Vec3
from data.model.types.core.vec4 import Vec4
from data.model.types.transform_components.mesh_components.bone_weights import BoneWeight


class VertexData:
    def __init__(self,
                 position: Vec3,
                 uv: Vec2 | None = None,
                 uv2: Vec2 | None = None,
                 normal: Vec3 | None = None,
                 tangent: Vec4 | None = None,
                 vertex_color: ColorByte | None = None,
                 bone_weight: BoneWeight | None = None):
        self.position: Vec3 = position

        self.uv: Vec2 | None = uv
        self.uv2: Vec2 | None = uv2
        self.normal: Vec3 | None = normal
        self.tangent: Vec4 | None = tangent
        self.vertex_color: ColorByte | None = vertex_color
        self.bone_weight: BoneWeight | None = bone_weight
