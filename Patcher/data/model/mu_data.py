from collections import deque
from copy import deepcopy
from pathlib import Path

from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.int3 import Int3
from data.model.types.core.vec2 import Vec2
from data.model.types.core.vec3 import Vec3
from data.model.types.material.material_property import MaterialPropertyTexture, MaterialProperty
from data.model.types.tag.tag_material_property import MaterialPropertyTag
from data.model.types.material.materials import Materials
from data.model.types.texture.texture import Texture
from data.model.types.texture.textures import Textures
from data.model.types.tag.tag_mu import MuTag
from data.model.types.transform import Transform
from data.model.types.transform_components.mesh_components.vertex_data import VertexData
from utils.exceptions import AttributeNotFoundError, AttributeInvalidError, ArgumentException
from utils.team_color import TeamColor


class MuData:
    def __init__(self,
                 name: str,
                 root_transform: Transform,
                 materials: Materials,
                 textures: Textures):
        self.name = name
        self.root_transform = root_transform
        self.materials = materials
        self.textures = textures

    @staticmethod
    def read(reader: ByteReader) -> 'MuData':
        name = reader.read_str()
        root_transform = Transform.read(reader)
        materials = Materials.read(reader)
        textures = Textures.read(reader)

        return MuData(name, root_transform, materials, textures)

    def __str__(self) -> str:
        return self.name

    def write_bytes(self, writer: ByteWriter | None = None) -> bytes:
        if writer is None:
            writer = ByteWriter()

        writer.write_str(self.name)

        self.root_transform.write(writer)

        self.materials.write(writer)
        self.textures.write(writer)

        return writer.output_data

    def write_file(self, filename: Path):
        writer: ByteWriter = ByteWriter()

        output = self.write_bytes(writer)
        with open(filename, "wb") as f:
            f.write(output)

    @staticmethod
    def from_bytes(data: bytes) -> 'MuData':
        reader = ByteReader(data)
        mu_file = MuData.read(reader)
        return mu_file

    @staticmethod
    def from_file(filename: Path) -> 'MuData':
        with open(filename, "rb") as f:
            data = f.read()

        reader = ByteReader(data)
        mu_file = MuData.read(reader)
        return mu_file

    # Accessors
    def get_transforms(self, transform_name: str | None = None, filter_type: set[MuTag] | MuTag | None = None) -> list[Transform]:
        output = []

        queue: deque[Transform] = deque()
        queue.append(self.root_transform)

        while len(queue) > 0:
            transform: Transform = queue.pop()
            if transform.name == transform_name or transform_name is None:
                if filter_type is None:
                    output.append(transform)
                else:
                    if isinstance(filter_type, set):
                        for tag in filter_type:
                            if tag in transform:
                                output.append(transform)
                                break
                    else:
                        if filter_type in transform:
                            output.append(transform)

            for child in transform.children:
                queue.append(child)

        return output

    # Modifications - Transforms
    def copy_transform(self, transform_name: str, new_name: str) -> Transform:
        if self.root_transform.name == transform_name:
            raise ArgumentException("Cannot copy root transform")

        queue: deque[list[Transform]] = deque()
        queue.append(self.root_transform.children)

        while len(queue) > 0:
            mu_transforms: list[Transform] = queue.pop()
            for index, child in enumerate(mu_transforms):
                if child.name == transform_name:
                    copy = deepcopy(child)
                    copy.name = new_name
                    mu_transforms.append(copy)
                    return copy

                queue.append(child.children)

        raise ArgumentException(f"No transforms were found with the name {transform_name}")

    def set_parent(self, parent_name: str, transform_names: list[str]):
        if self.root_transform.name in transform_names:
            raise ArgumentException("Cannot set root transform parent to child")

        parents = self.get_transforms(parent_name, None)
        if len(parents) == 0:
            raise ArgumentException(f"No transforms were found with the name {parent_name}")

        parent = parents[0]

        queue: deque[list[Transform]] = deque()
        queue.append(self.root_transform.children)

        while len(queue) > 0:
            mu_transforms: list[Transform] = queue.pop()
            for index, child in enumerate(mu_transforms):
                if child.name in transform_names:
                    parent.children.append(mu_transforms[index])
                    del mu_transforms[index]
                else:
                    queue.append(child.children)

    def remove_transform(self, transform_name: str):
        if self.root_transform.name == transform_name:
            raise ArgumentException("Cannot remove root transform")

        transforms = self.get_transforms(transform_name)
        if len(transforms) == 0:
            raise ArgumentException(f"No transforms were found with the name {transform_name}")

        self.remove_transforms(transforms)

    def remove_transforms(self, transform_names: list[Transform]):
        queue: deque[list[Transform]] = deque()
        queue.append(self.root_transform.children)

        transforms_remaining: int = len(transform_names)

        while len(queue) > 0:
            mu_transforms: list[Transform] = queue.pop()
            for index, child in enumerate(mu_transforms):
                for transform in transform_names:
                    if child is transform:
                        del mu_transforms[index]
                        transforms_remaining -= 1
                        if transforms_remaining == 0:
                            return

                queue.append(child.children)

    # Modifications - Transform Mesh Data
    def copy_triangles(self, source: str, destination: str | None, triangle_indices: list[int]):
        mesh_transforms_source = self.get_transforms(source, MuTag.MeshFilter)
        mesh_source = mesh_transforms_source[0][MuTag.MeshFilter]

        split_triangles_temp: list[Int3] = []
        for index in triangle_indices:
            split_triangles_temp.append(mesh_source.triangles[index])

        used_vertex_indices: set[int] = set()
        for triangle in split_triangles_temp:
            used_vertex_indices.add(triangle.x)
            used_vertex_indices.add(triangle.y)
            used_vertex_indices.add(triangle.z)

        split_vertex_data: list[VertexData] = []
        mapping: dict[int, int] = {}
        new_index = 0
        for index, vertex_data in enumerate(mesh_source.vertex_data):
            if index in used_vertex_indices:
                split_vertex_data.append(deepcopy(vertex_data))
                mapping[index] = new_index
                new_index += 1

        split_triangles: list[Int3] = []
        for triangle in split_triangles_temp:
            split_triangles.append(
                Int3(
                    mapping[triangle.x],
                    mapping[triangle.y],
                    mapping[triangle.z],
                )
            )

        if destination is None:
            offset = len(mesh_source.vertex_data)
            for i in range(len(split_triangles)):
                split_triangles[i] = Int3(
                    split_triangles[i].x + offset,
                    split_triangles[i].y + offset,
                    split_triangles[i].z + offset,
                )

            mesh_source.vertex_data.extend(split_vertex_data)
            mesh_source.triangles.extend(split_triangles)
        else:
            mesh_transforms_dest = self.get_transforms(destination, MuTag.MeshFilter)
            mesh_dest = mesh_transforms_dest[0][MuTag.MeshFilter]

            dest_num_vertices = len(mesh_dest.vertex_data)
            for i in range(len(split_triangles)):
                split_triangles[i] = Int3(
                    split_triangles[i].x + dest_num_vertices,
                    split_triangles[i].y + dest_num_vertices,
                    split_triangles[i].z + dest_num_vertices,
                )

            mesh_dest.vertex_data.extend(split_vertex_data)
            mesh_dest.triangles.extend(split_triangles)

    def remove_triangles(self, source: str, triangle_indices: list[int]):
        mesh_transforms_source = self.get_transforms(source, MuTag.MeshFilter)
        mesh_source = mesh_transforms_source[0][MuTag.MeshFilter]

        vert_indices_to_keep: set[int] = set()

        remove_triangles: list[Int3] = []
        for index in reversed(range(len(mesh_source.triangles))):
            triangle = mesh_source.triangles[index]
            if index in triangle_indices:
                remove_triangles.append(triangle)
                del mesh_source.triangles[index]
            else:
                vert_indices_to_keep.add(triangle.x)
                vert_indices_to_keep.add(triangle.y)
                vert_indices_to_keep.add(triangle.z)

        new_index = 0
        mapping: dict[int, int] = {}
        for index in range(len(mesh_source.vertex_data)):
            if index in vert_indices_to_keep:
                mapping[index] = new_index
                new_index += 1

        for index in reversed(range(len(mesh_source.vertex_data))):
            if index not in vert_indices_to_keep:
                del mesh_source.vertex_data[index]

        for triangle_index in range(len(mesh_source.triangles)):
            triangle_current = mesh_source.triangles[triangle_index]
            mesh_source.triangles[triangle_index] = Int3(
                mapping[triangle_current.x],
                mapping[triangle_current.y],
                mapping[triangle_current.z],
            )

    def edit_vertices(self, mesh_name: str, positions: dict[int, Vec3]):
        transforms = self.get_transforms(mesh_name, MuTag.MeshFilter)
        if len(transforms) == 0:
            raise ArgumentException(f"No mesh-data-containing transforms were found with the name {mesh_name}")

        for transform in transforms:
            mesh = transform[MuTag.MeshFilter]

            for index, position in positions.items():
                mesh.vertex_data[index].position = position

    def edit_uvs(self, mesh_name: str, uvs: dict[int, Vec2], is_uv2: bool = False):
        transforms = self.get_transforms(mesh_name, MuTag.MeshFilter)
        if len(transforms) == 0:
            raise ArgumentException(f"No mesh-data-containing transforms were found with the name {mesh_name}")

        for transform in transforms:
            mesh = transform[MuTag.MeshFilter]

            for index, uv in uvs.items():
                if is_uv2:
                    mesh.vertex_data[index].uv2 = uv
                else:
                    mesh.vertex_data[index].uv = uv

    def edit_normals(self, mesh_name: str, normals: dict[int, Vec3]):
        transforms = self.get_transforms(mesh_name, MuTag.MeshFilter)
        if len(transforms) == 0:
            raise ArgumentException(f"No mesh-data-containing transforms were found with the name {mesh_name}")

        for transform in transforms:
            mesh = transform[MuTag.MeshFilter]

            for index, normal in normals.items():
                mesh.vertex_data[index].normal = normal

    def edit_normals_average(self, mesh_name: str, vertex_indices: list[list[int]]):
        transforms = self.get_transforms(mesh_name, MuTag.MeshFilter)
        if len(transforms) == 0:
            raise ArgumentException(f"No mesh-data-containing transforms were found with the name {mesh_name}")

        for transform in transforms:
            mesh = transform[MuTag.MeshFilter]

            for group in vertex_indices:
                normal_sum = Vec3(0, 0, 0)

                for vertex_index in group:
                    normal_sum += mesh.vertex_data[vertex_index].normal

                normal_sum /= len(vertex_indices)
                normal_sum = normal_sum.normalize()

                for vertex_index in group:
                    mesh.vertex_data[vertex_index].normal = normal_sum

    # Accessors - Textures
    def get_texture_index(self, texture_name: str):
        for index, texture in enumerate(self.textures):
            if texture.name == texture_name:
                return index

        return -1

    # Modifications - Materials
    def assign_material(self, mesh_name: str, material_name: str):
        mat_index = self.materials.get_index(material_name)
        if mat_index == -1:
            raise ArgumentException(f"Material {material_name} was not found")

        transforms = self.get_transforms(mesh_name, MuTag.MeshRenderer)
        if len(transforms) == 0:
            raise ArgumentException(f"No mesh-data-containing transforms were found with the name {mesh_name}")

        for transform in transforms:
            renderer = transform[MuTag.MeshRenderer]
            renderer.material_index = mat_index

    def copy_material(self, material_name: str, new_material_name: str):
        src_material = self.materials[material_name]
        material_copy = deepcopy(src_material)
        material_copy.name = new_material_name
        self.materials.append(material_copy)

    def edit_material_shader(self, material_name: str, shader_name: str):
        material = self.materials[material_name]
        material.shader_name = shader_name

    def add_texture_map(self, material_name: str, prop_name: str, suffix: str, is_normal_map: bool = False):
        material = self.materials[material_name]

        main_tex_prop = material.get_main_tex_prop()

        new_tex_name = str(Path(self.textures[main_tex_prop.index].name).with_suffix(""))
        if new_tex_name.endswith("-a"):
            new_tex_name = new_tex_name[:-2]

        new_tex_name += "-" + suffix

        new_tex_prop = deepcopy(main_tex_prop)
        new_tex_prop.name = prop_name

        tex_index = self.get_texture_index(new_tex_name)
        if tex_index != -1:
            new_tex_prop.index = tex_index
        else:
            new_tex_prop.index = len(self.textures)
            self.textures.append(Texture(name=new_tex_name, is_normal_map=is_normal_map))

        material.properties.append(new_tex_prop)

    def split_texture(self, material_name: str, prop_name: str, new_texture_name: str):
        material = self.materials[material_name]
        texture_prop = MaterialProperty.get_texture(material.properties, prop_name)

        self.textures.append(Texture(name=new_texture_name, is_normal_map=self.textures[texture_prop.index].is_normal_map))
        texture_prop.index = len(self.textures) - 1

    def assign_team_colors(self, material_name: str, tc1: TeamColor, tc2: TeamColor):
        material = self.materials[material_name]
        if material.shader_name != "Resurfaced/Standard (TC)":
            material.shader_name = "Resurfaced/Standard (TC)"

            main_tex_prop = material.get_main_tex_prop()
            main_tex_file_name = str(Path(self.textures[main_tex_prop.index].name).with_suffix(""))

            if not main_tex_file_name.endswith("-a"):
                self.textures[main_tex_prop.index].name = main_tex_file_name + "-a"

            if "_BumpMap" not in [x.name for x in material.properties]:
                self.add_texture_map(material.name, "_BumpMap", "n")

            self.add_texture_map(material.name, "_MetalMap", "m")
            self.add_texture_map(material.name, "_TeamColorMap", "tc")

            material.remove_property("_SpecMap")

        material.add_or_update_property(prop_name="_TC1Color", prop_type=MaterialPropertyTag.Color, prop_value=tc1.color)
        material.add_or_update_property(prop_name="_TC1Metalness", prop_type=MaterialPropertyTag.Float3, prop_value=tc1.metalness)
        material.add_or_update_property(prop_name="_TC1Smoothness", prop_type=MaterialPropertyTag.Float3, prop_value=tc1.smoothness)
        material.add_or_update_property(prop_name="_TC1MetalBlend", prop_type=MaterialPropertyTag.Float3, prop_value=tc1.metal_blend)
        material.add_or_update_property(prop_name="_TC1SmoothBlend", prop_type=MaterialPropertyTag.Float3, prop_value=tc1.smooth_blend)

        material.add_or_update_property(prop_name="_TC2Color", prop_type=MaterialPropertyTag.Color, prop_value=tc2.color)
        material.add_or_update_property(prop_name="_TC2Metalness", prop_type=MaterialPropertyTag.Float3, prop_value=tc2.metalness)
        material.add_or_update_property(prop_name="_TC2Smoothness", prop_type=MaterialPropertyTag.Float3, prop_value=tc2.smoothness)
        material.add_or_update_property(prop_name="_TC2MetalBlend", prop_type=MaterialPropertyTag.Float3, prop_value=tc2.metal_blend)
        material.add_or_update_property(prop_name="_TC2SmoothBlend", prop_type=MaterialPropertyTag.Float3, prop_value=tc2.smooth_blend)

    def remove_material(self, material_name: str):
        target_index = self.materials.get_index(material_name)
        if target_index == -1:
            raise AttributeNotFoundError(f'Material with name {material_name} not found in model')

        transforms = self.get_transforms(transform_name=None, filter_type=MuTag.MeshRenderer)
        renderers = [x[MuTag.MeshRenderer] for x in transforms]

        for index, renderer in enumerate(renderers):
            if renderer.material_index == target_index:
                raise AttributeInvalidError(f"Cannot remove material {material_name}: Transform with name {transforms[index].name} currently references it")

            # Reindex material references
            if renderer.material_index > target_index:
                renderer.material_index -= 1

        del self.materials[target_index]

    # Modifications - Textures
    def rename_texture(self, texture_name: str, new_texture_name: str):
        self.textures[texture_name].name = new_texture_name

    def remove_texture(self, texture_name: str):
        tex_index = self.textures.get_index(texture_name)
        for material in self.materials:
            for prop in material.properties:
                if not isinstance(prop, MaterialPropertyTexture):
                    continue

                if prop.index < tex_index:
                    continue

                prop.index -= 1

        del self.textures[tex_index]
