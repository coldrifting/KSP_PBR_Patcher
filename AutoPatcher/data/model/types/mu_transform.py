from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec3 import Vec3
from data.model.types.core.vec4 import Vec4
from data.model.types.mu_tag import MuTag
from data.model.types.transform.collider.collider_data import ColliderData
from data.model.types.transform.anim_data import AnimData
from data.model.types.transform.light_data import LightData
from data.model.types.transform.mesh.mesh_data import MeshData
from data.model.types.transform.skinned_mesh_data import SkinnedMeshData


class Transform:
    def __init__(self,
                 name: str,
                 position: Vec3,
                 rotation: Vec4,
                 scale: Vec3,
                 unity_tag: str,
                 unity_layer: int,
                 collider: ColliderData | None = None,
                 mesh_data: MeshData | None = None,
                 anim_data: AnimData | None = None,
                 skinned_mesh_data: SkinnedMeshData | None = None,
                 light_data: LightData | None = None,
                 children: list['Transform'] | None = None):
        self.name = name
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.unity_tag = unity_tag
        self.unity_layer = unity_layer
        self.collider: ColliderData | None = collider
        self.mesh_data: MeshData | None = mesh_data
        self.anim_data: AnimData | None = anim_data
        self.skinned_mesh_data: SkinnedMeshData | None = skinned_mesh_data
        self.light_data: LightData | None = light_data

        self.children: list[Transform] = [] if children is None else children

    def __str__(self) -> str:
        return self.name

    def clone(self, new_transform_name: str, clear_mesh_data: bool = False) -> 'Transform':
        mesh_data = self.mesh_data.clone(clear_mesh_data) if self.mesh_data is not None else None
        return Transform(
            name = new_transform_name,
            position = self.position.clone(),
            rotation = self.rotation.clone(),
            scale = self.scale.clone(),
            unity_tag = self.unity_tag,
            unity_layer = self.unity_layer,

            mesh_data = mesh_data
        )

    def write(self, writer: ByteWriter):
        writer.write_str(self.name)

        writer.write_vec3(self.position)
        writer.write_vec4(self.rotation)
        writer.write_vec3(self.scale)

        writer.write_int(MuTag.UnityTagAndLayer)
        writer.write_str(self.unity_tag)
        writer.write_int(self.unity_layer)

        if self.collider is not None:
            self.collider.write(writer)

        if self.mesh_data is not None:
            writer.write_int(MuTag.MeshFilter)
            self.mesh_data.write(writer)

        if self.anim_data is not None:
            self.anim_data.write(writer)

        if self.skinned_mesh_data is not None:
            self.skinned_mesh_data.write(writer)

        if self.light_data is not None:
            self.light_data.write(writer)

        if len(self.children) > 0:
            for child in self.children:
                writer.write_int(MuTag.ChildTransformStart)
                child.write(writer)
                writer.write_int(MuTag.ChildTransformEnd)

    @staticmethod
    def read(reader: ByteReader) -> 'Transform':
        name = reader.read_str()

        position = reader.read_vec3()
        rotation = reader.read_vec4()
        scale = reader.read_vec3()

        reader.read_int() # Consume Unity Tag
        unity_tag = reader.read_str()
        unity_layer = reader.read_int()

        collider = None
        if reader.preview() in ColliderData.tags():
            collider = ColliderData.read(reader)

        mesh_data = None
        if reader.preview() == MuTag.MeshFilter:
            reader.read_int()  # Consume Tag
            mesh_data = MeshData.read(reader)

        anim_data = AnimData.read(reader) if reader.preview() == MuTag.Animation else None
        skinned_mesh_data = SkinnedMeshData.read(reader) if reader.preview() == MuTag.SkinnedMeshRenderer else None
        light_data = LightData.read(reader) if reader.preview() == MuTag.Light else None

        children = []
        if reader.preview() == MuTag.ChildTransformStart:
            while reader.has_data() and reader.preview() == MuTag.ChildTransformStart:
                reader.read_int() # Consume Tag.ChildTransformStart
                children.append(Transform.read(reader))
                tag = reader.read_int() # Consume Tag.ChildTransformEnd
                if tag != MuTag.ChildTransformEnd:
                    raise Exception(f"ChildTransformEnd tag expected, but {MuTag(tag)} tag found")

        if reader.preview(4) == MuTag.Materials:
            pass

        return Transform(
            name = name,
            position = position,
            rotation = rotation,
            scale = scale,
            unity_tag = unity_tag,
            unity_layer = unity_layer,
            collider = collider,
            mesh_data = mesh_data,
            anim_data = anim_data,
            skinned_mesh_data = skinned_mesh_data,
            light_data = light_data,
            children = children
        )