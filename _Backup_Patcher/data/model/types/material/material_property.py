from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec2 import Vec2
from data.model.types.core.vec4 import Vec4
from data.model.types.tag.tag_material_property import MaterialPropertyTag
from utils.exceptions import ArgumentException


class MaterialProperty:
    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def read(reader: ByteReader) -> 'MaterialProperty':
        name = reader.read_str()
        property_type = MaterialPropertyTag(reader.read_int())
        match property_type:
            case MaterialPropertyTag.Color:
                return MaterialPropertyColor(name=name, value=reader.read_vec4())
            case MaterialPropertyTag.Vector:
                return MaterialPropertyVector(name=name, value=reader.read_vec4())
            case MaterialPropertyTag.Float2:
                return MaterialPropertyFloat2(name=name, value=reader.read_float())
            case MaterialPropertyTag.Float3:
                return MaterialPropertyFloat3(name=name, value=reader.read_float())
            case MaterialPropertyTag.Texture:
                index = reader.read_int()
                scale = reader.read_vec2()
                offset = reader.read_vec2()
                return MaterialPropertyTexture(name=name, index=index, scale=scale, offset=offset)
            case _:
                raise Exception(f"Unknown material property type {property_type} for property {name}")

    def write(self, writer: ByteWriter):
        writer.write_str(self.name)
        match self:
            case MaterialPropertyColor() as prop_color:
                writer.write_int(MaterialPropertyTag.Color)
                writer.write_vec4(prop_color.value)
            case MaterialPropertyVector() as prop_vector:
                writer.write_int(MaterialPropertyTag.Vector)
                writer.write_vec4(prop_vector.value)
            case MaterialPropertyFloat2() as prop_float2:
                writer.write_int(MaterialPropertyTag.Float2)
                writer.write_float(prop_float2.value)
            case MaterialPropertyFloat3() as prop_float3:
                writer.write_int(MaterialPropertyTag.Float3)
                writer.write_float(prop_float3.value)
            case MaterialPropertyTexture() as prop_texture:
                writer.write_int(MaterialPropertyTag.Texture)
                writer.write_int(prop_texture.index)
                writer.write_vec2(prop_texture.scale)
                writer.write_vec2(prop_texture.offset)

    # Accessors
    @staticmethod
    def get_texture(properties: list['MaterialProperty'], prop_name: str) -> 'MaterialPropertyTexture':
        for prop in properties:
            if prop.name == prop_name:
                if isinstance(prop, MaterialPropertyTexture):
                    return prop
                raise ArgumentException(f"Prop with name {prop_name} is not a texture property")

        raise ArgumentException(f"Prop with name {prop_name} does not exist")


class MaterialPropertyColor(MaterialProperty):
    def __init__(self, name: str, value: Vec4):
        super().__init__(name=name)
        self.value = value

class MaterialPropertyVector(MaterialProperty):
    def __init__(self, name: str, value: Vec4):
        super().__init__(name=name)
        self.value = value

class MaterialPropertyFloat2(MaterialProperty):
    def __init__(self, name: str, value: float | int):
        super().__init__(name=name)
        self.value = value

class MaterialPropertyFloat3(MaterialProperty):
    def __init__(self, name: str, value: float | int):
        super().__init__(name=name)
        self.value = value

class MaterialPropertyTexture(MaterialProperty):
    def __init__(self, name: str, index: int, scale: Vec2, offset: Vec2):
        super().__init__(name=name)
        self.index = index
        self.scale = scale
        self.offset = offset
