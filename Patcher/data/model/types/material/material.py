from typing import Any

from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec2 import Vec2
from data.model.types.material.material_property import MaterialProperty, MaterialPropertyTexture, \
    MaterialPropertyFloat3, MaterialPropertyColor, MaterialPropertyFloat2, MaterialPropertyVector
from data.model.types.tag.tag_material_property import MaterialPropertyTag
from data.model.types.tag.tag_material import MaterialTag
from utils.exceptions import ArgumentException


class Material:
    def __init__(self, name: str, shader_name: str, properties: list[MaterialProperty]):
        self.name = name
        self.shader_name = shader_name
        self.properties = properties

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def read(reader: ByteReader) -> 'Material':
        name: str = reader.read_str()
        if reader.mu_version <= 3:
            mat_type = MaterialTag(reader.read_int())
            shader_name = mat_type.get_shader_name()
            properties = mat_type.read_properties(reader)

        else:
            shader_name = reader.read_str()

            properties = []
            properties_count = reader.read_int()
            for i in range(properties_count):
                prop = MaterialProperty.read(reader)
                properties.append(prop)

        return Material(name=name,
                        shader_name=shader_name,
                        properties=properties)

    def write(self, writer: ByteWriter):
        writer.write_str(self.name)
        writer.write_str(self.shader_name)
        writer.write_int(len(self.properties))
        for prop in self.properties:
            prop.write(writer)

    # Accessors
    def get_main_tex_prop(self) -> MaterialPropertyTexture:
        for prop in self.properties:
            if prop.name == "_MainTex":
                if isinstance(prop, MaterialPropertyTexture):
                    return prop

        raise ArgumentException("_MainTex property not found")

    # Modifications
    def add_or_update_property(self, prop_name: str, prop_type: MaterialPropertyTag, prop_value: Any):
        if prop_name in [x.name for x in self.properties]:
            index = [x.name for x in self.properties].index(prop_name)
            prop = self.properties[index]

            match prop:
                case MaterialPropertyColor():
                    prop.value = prop_value
                case MaterialPropertyFloat3():
                    prop.value = prop_value
                case MaterialPropertyTexture():
                    prop.index = prop_value
                case _:
                    raise NotImplementedError

        else:
            match prop_type:
                case MaterialPropertyTag.Color:
                    self.properties.append(MaterialPropertyColor(prop_name, prop_value))
                case MaterialPropertyTag.Vector:
                    self.properties.append(MaterialPropertyVector(prop_name, prop_value))
                case MaterialPropertyTag.Float2:
                    self.properties.append(MaterialPropertyFloat2(prop_name, prop_value))
                case MaterialPropertyTag.Float3:
                    self.properties.append(MaterialPropertyFloat3(prop_name, prop_value))
                case MaterialPropertyTag.Texture:
                    self.properties.append(
                        MaterialPropertyTexture(prop_name, prop_value, Vec2(1, 1), Vec2(0, 0)))

                case _:
                    raise NotImplementedError

