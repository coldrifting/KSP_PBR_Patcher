from collections import deque
from pathlib import Path
from typing import Any

from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec2 import Vec2
from data.model.types.material.material import Material
from data.model.types.material.material_property import MaterialProperty, MaterialPropertyColor, MaterialPropertyVector, \
    MaterialPropertyFloat2, MaterialPropertyFloat3, MaterialPropertyTexture
from data.model.types.material.texture import Texture
from data.model.types.mu_tag import MuTag
from data.model.types.mu_transform import Transform
from data.model.types.transform.mesh.mesh_data import MeshData
from utils.exceptions import AttributeNotFoundError, AttributeInvalidError


class MuFile:
    def __init__(self, name: str, root_transform: Transform, materials: list[Material] | None = None, textures: list[Texture] | None = None):
        self.name = name

        self.root_transform = root_transform
        self.materials = [] if materials is None else materials
        self.textures = [] if textures is None else textures

    def __str__(self) -> str:
        return self.name

    def get_transform(self, transform_name: str) -> Transform:
        queue: deque[Transform] = deque()
        queue.append(self.root_transform)

        while len(queue) > 0:
            transform: Transform = queue.pop()
            if transform.name == transform_name:
                return transform

            for child in transform.children:
                queue.append(child)

        raise AttributeNotFoundError(f'Transform with name {transform_name} not found in file')

    def get_mesh(self, mesh_name: str) -> MeshData:
        queue: deque[Transform] = deque()
        queue.append(self.root_transform)

        while len(queue) > 0:
            transform: Transform = queue.pop()
            if transform.name == mesh_name:
                if transform.mesh_data is not None:
                    return transform.mesh_data
                break

            for child in transform.children:
                queue.append(child)

        raise AttributeNotFoundError(f'Transform with mesh data with name {mesh_name} not found in file')

    def clone_transform(self, transform_name: str, new_transform_name: str, clear_mesh_data: bool = False) -> Transform:
        queue: deque[list[Transform]] = deque()
        queue.append(self.root_transform.children)

        while len(queue) > 0:
            transforms: list[Transform] = queue.pop()
            for child in transforms:
                if child.name == transform_name:
                    new_transform = child.clone(new_transform_name, clear_mesh_data)
                    transforms.append(new_transform)
                    return new_transform

                queue.append(child.children)

        raise AttributeNotFoundError(f'Transform with name {transform_name} not found in file')

    def delete_transform(self, transform_name: str):
        queue: deque[list[Transform]] = deque()
        queue.append(self.root_transform.children)

        while len(queue) > 0:
            transforms: list[Transform] = queue.pop()
            for index, child in enumerate(transforms):
                if child.name == transform_name:
                    del transforms[index]
                    return

                queue.append(child.children)

        raise AttributeNotFoundError(f'Transform with name {transform_name} not found in file')


    def merge_transforms(self, transform_name_primary: str, transform_name_secondary: str):
        if len(self.root_transform.children) == 0:
            raise AttributeInvalidError("Root transform has no children and can not be merged")

        primary_mesh = self.get_mesh(transform_name_primary)
        secondary_mesh = self.get_mesh(transform_name_secondary)

        primary_mesh.merge(secondary_mesh)
        self.delete_transform(transform_name_secondary)


    def get_material(self, material_name) -> Material:
        for material in self.materials:
            if material.name == material_name:
                return material

        raise AttributeNotFoundError(f'Material with name {material_name} not found in file')

    def get_material_index(self, material_name) -> int:
        for index, material in enumerate(self.materials):
            if material.name == material_name:
                return index

        raise AttributeNotFoundError(f'Material with name {material_name} not found in file')

    def has_property(self, material_name, property_name) -> bool:
        material = self.get_material(material_name)
        for material_property in material.properties:
            if material_property.name == property_name:
                return True

        return False

    def get_property(self, material_name, property_name) -> MaterialProperty:
        material = self.get_material(material_name)
        for material_property in material.properties:
            if material_property.name == property_name:
                return material_property

        raise AttributeNotFoundError(f'Material property with name {property_name} not found in material {material_name}')

    def get_texture_index(self, texture_name) -> int:
        for index, texture in enumerate(self.textures):
            if texture.name == texture_name:
                return index

        raise AttributeNotFoundError(f'Texture with name {texture_name} not found in file. Did you forget a file extension?')

    def get_texture(self, texture_name):
        texture_index = self.get_texture_index(texture_name)
        return self.textures[texture_index]

    def add_property(self, material_name: str, property_name: str, property_type: str, value: Any):
        mat = self.get_material(material_name)

        has_prop = self.has_property(material_name, property_name)
        if has_prop:
            raise AttributeError(f'Material property with name {property_name} already exists for material {material_name}')

        match property_type:
            case "color":
                mat.properties.append(MaterialPropertyColor(property_name, value))
            case "vector":
                mat.properties.append(MaterialPropertyVector(property_name, value))
            case "float2":
                mat.properties.append(MaterialPropertyFloat2(property_name, value))
            case "float3":
                mat.properties.append(MaterialPropertyFloat3(property_name, value))
            case "float":
                mat.properties.append(MaterialPropertyFloat3(property_name, value))
            case "texture":
                mat.properties.append(MaterialPropertyTexture(property_name, self.get_texture_index(value), Vec2(1,1), Vec2(0,0)))

    def edit_property(self, material_name: str, property_name: str, value) -> None:
        prop = self.get_property(material_name, property_name)

        match prop:
            case MaterialPropertyColor():
                prop.color = value
            case MaterialPropertyVector():
                prop.value = value
            case MaterialPropertyFloat2():
                prop.value = value
            case MaterialPropertyFloat3():
                prop.value = value
            case MaterialPropertyTexture():
                prop.texture_index = self.get_texture_index(value)

    def write(self, writer: ByteWriter | None = None) -> bytes:
        # Allow passing in a custom writer for testing
        if writer is None:
            writer = ByteWriter()

        # Mu file identifier and version number
        writer.write_byte(0xFF)
        writer.write_byte(0x2A)
        writer.write_byte(0x01)
        writer.write_byte(0x00)
        writer.write_int(5)

        writer.write_str(self.name)

        self.root_transform.write(writer)

        if len(self.materials) > 0:
            writer.write_int(MuTag.Materials)
            writer.write_int(len(self.materials))
            for material in self.materials:
                material.write(writer)

        if len(self.textures) > 0:
            writer.write_int(MuTag.Textures)
            writer.write_int(len(self.textures))
            for texture in self.textures:
                texture.write(writer)

        return writer.output_data

    @staticmethod
    def read(reader: ByteReader) -> 'MuFile':
        # Skip Header
        reader.read_int()
        reader.read_int()

        name = reader.read_str()

        root_transform = Transform.read(reader)

        materials: list[Material] = []
        if reader.has_data() and reader.preview() == MuTag.Materials:
            reader.read_int()  # Consume the tag
            materials_count = reader.read_int()
            for i in range(materials_count):
                material = Material.read(reader)
                materials.append(material)

        textures: list[Texture] = []
        if reader.has_data() and reader.preview() == MuTag.Textures:
            reader.read_int()  # Consume the tag
            textures_count = reader.read_int()
            for i in range(textures_count):
                texture = Texture.read(reader)
                textures.append(texture)

        return MuFile(
            name = name,
            root_transform = root_transform,
            materials = materials,
            textures = textures
        )

    def write_file(self, filename: Path):
        output = self.write()
        with open(filename, "wb") as f:
            f.write(output)

    @staticmethod
    def read_file(filename: Path) -> 'MuFile':
        with open(filename, "rb") as f:
            data = f.read()

        reader = ByteReader(data)
        mu_file = MuFile.read(reader)
        return mu_file