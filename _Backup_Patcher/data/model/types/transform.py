from typing import Literal, overload

from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec3 import Vec3
from data.model.types.core.vec4 import Vec4
from data.model.types.generic.mu_component import MuComponent
from data.model.types.tag.tag_mu import MuTag
from data.model.types.transform_components.animation import Animation
from data.model.types.transform_components.collider.box import ColliderBox
from data.model.types.transform_components.collider.capsule import ColliderCapsule
from data.model.types.transform_components.collider.mesh import ColliderMesh
from data.model.types.transform_components.collider.sphere import ColliderSphere
from data.model.types.transform_components.collider.wheel import ColliderWheel
from data.model.types.transform_components.light import Light
from data.model.types.transform_components.mesh import Mesh
from data.model.types.transform_components.particles import Particles
from data.model.types.transform_components.renderer import MeshRenderer
from data.model.types.transform_components.skinned_mesh import SkinnedMesh
from data.model.types.transform_components.unity_info import UnityInfo
from utils.printing import warn


class Transform:
    def __init__(self,
                 name: str,
                 position: Vec3 | None = None,
                 rotation: Vec4 | None = None,
                 scale: Vec3 | None = None,
                 data: dict[MuTag, MuComponent] | None = None,
                 children: list['Transform'] | None = None):
        self.name = name
        self.position = position if position is not None else Vec3(0, 0, 0)
        self.rotation = rotation if rotation is not None else Vec4(0, 0, 0, 1)
        self.scale = scale if scale is not None else Vec3(1, 1, 1)
        self.data: dict[MuTag, MuComponent] = data if data is not None else {MuTag.UnityInfo: UnityInfo("Untagged", 0)}
        self.children: list['Transform'] = children if children is not None else []

    def __str__(self) -> str:
        return self.name

    @overload
    def __getitem__(self, tag: Literal[MuTag.UnityInfo]) -> UnityInfo:
        ...

    @overload
    def __getitem__(self, tag: Literal[MuTag.MeshRenderer]) -> MeshRenderer:
        ...

    @overload
    def __getitem__(self, tag: Literal[MuTag.SkinnedMeshRenderer]) -> SkinnedMesh:
        ...

    @overload
    def __getitem__(self, tag: Literal[MuTag.MeshFilter]) -> Mesh:
        ...

    @overload
    def __getitem__(self, tag: Literal[MuTag.Particles]) -> Particles:
        ...

    @overload
    def __getitem__(self, tag: MuTag) -> MuComponent:
        ...

    def __getitem__(self, tag: MuTag) -> MuComponent:
        item: MuComponent | None = self.data.get(tag, None)
        if item is None:
            raise KeyError(f"Component with tag {tag} not found for transform {self.name}")

        return item

    def __contains__(self, tag: MuTag) -> bool:
        return self.data.__contains__(tag)

    @staticmethod
    def read(reader: ByteReader) -> 'Transform':
        name = reader.read_str()
        position: Vec3 = reader.read_vec3()
        rotation: Vec4 = reader.read_vec4()
        scale: Vec3 = reader.read_vec3()

        data: dict[MuTag, MuComponent] = {}
        children: list[Transform] = []

        if reader.mu_version <= 2:
            reader.read_float() # Consume extra unknown value

        while True:
            tag_num = None
            try:
                tag: MuTag = reader.read_tag()
            except ValueError:
                warn(f"Invalid tag {tag_num} at position 0x{reader.pointer:X}")
                raise
            except EOFError:
                break
            match tag:
                case MuTag.ChildTransformStart:
                    if reader.read_int() == MuTag.ChildTransformEnd:
                        break
                    else:
                        reader.rewind(4)

                    child_transform = Transform.read(reader)
                    children.append(child_transform)
                case MuTag.ChildTransformEnd:
                    break

                case MuTag.UnityInfo:
                    data[tag] = UnityInfo.read(reader)

                case MuTag.MeshFilter:
                    data[tag] = Mesh.read(reader)
                case MuTag.MeshRenderer:
                    data[tag] = MeshRenderer.read(reader)

                case MuTag.ColliderBox:
                    data[tag] = ColliderBox.read(reader, False)
                case MuTag.ColliderBox2:
                    data[tag] = ColliderBox.read(reader, True)
                case MuTag.ColliderSphere:
                    data[tag] = ColliderSphere.read(reader, False)
                case MuTag.ColliderSphere2:
                    data[tag] = ColliderSphere.read(reader, True)
                case MuTag.ColliderCapsule:
                    data[tag] = ColliderCapsule.read(reader, False)
                case MuTag.ColliderCapsule2:
                    data[tag] = ColliderCapsule.read(reader, True)
                case MuTag.ColliderMesh:
                    data[tag] = ColliderMesh.read(reader, False)
                case MuTag.ColliderMesh2:
                    data[tag] = ColliderMesh.read(reader, True)
                case MuTag.ColliderWheel:
                    data[tag] = ColliderWheel.read(reader)

                case MuTag.Animation:
                    data[tag] = Animation.read(reader)
                case MuTag.SkinnedMeshRenderer:
                    data[tag] = SkinnedMesh.read(reader)
                case MuTag.Light:
                    data[tag] = Light.read(reader)
                case MuTag.Particles:
                    data[tag] = Particles.read(reader)

                case MuTag.Materials:
                    reader.rewind(4)
                    break

                case _:
                    raise NotImplementedError()

        return Transform(
            name=name,
            position=position,
            rotation=rotation,
            scale=scale,
            data=data,
            children=children
        )

    def write(self, writer: ByteWriter):
        writer.write_str(self.name)

        writer.write_vec3(self.position)
        writer.write_vec4(self.rotation)
        writer.write_vec3(self.scale)

        for tag, data in self.data.items():
            data.write(writer)

        if len(self.children) > 0:
            for child in self.children:
                writer.write_int(MuTag.ChildTransformStart)
                child.write(writer)
                writer.write_int(MuTag.ChildTransformEnd)

    # Modifications
    def assign_material_index(self, material_index: int):
        if MuTag.MeshRenderer in self:
            mesh = self[MuTag.MeshRenderer]
            mesh.material_index = material_index
        elif MuTag.SkinnedMeshRenderer in self:
            skinned_mesh = self[MuTag.SkinnedMeshRenderer]
            skinned_mesh.material_indices[0] = material_index # TODO - Should this be smarter?
        else:
            raise KeyError(f"Cannot assign material to transform {self.name}: it has no renderable components")

    def get_material_index(self) -> int:
        if MuTag.MeshRenderer in self:
            mesh = self[MuTag.MeshRenderer]
            return mesh.material_index
        elif MuTag.SkinnedMeshRenderer in self:
            skinned_mesh = self[MuTag.SkinnedMeshRenderer]
            return skinned_mesh.material_indices[0] # TODO - Should this be smarter?
        else:
            raise KeyError(f"Cannot get material index of transform {self.name}: it has no renderable components")
