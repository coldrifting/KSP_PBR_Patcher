from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.core.vec2 import Vec2
from data.model.types.core.vec4 import Vec4


class MaterialProperty:
    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name

    def clone(self: 'MaterialProperty') -> 'MaterialProperty':
        match self:
            case MaterialPropertyColor():
                return MaterialPropertyColor(self.name, self.color.clone())
            case MaterialPropertyVector():
                return MaterialPropertyVector(self.name, self.value)
            case MaterialPropertyFloat2():
                return MaterialPropertyFloat2(self.name, self.value)
            case MaterialPropertyFloat3():
                return MaterialPropertyFloat3(self.name, self.value)
            case MaterialPropertyTexture():
                return MaterialPropertyTexture(self.name, self.texture_index, self.scale.clone(), self.offset.clone())
        raise Exception(f"Unknown material property with name: {self.name}")

    def write_base(self, writer: ByteWriter):
        pass

    def write(self, writer: ByteWriter):
        self.write_base(writer)

    @staticmethod
    def read(reader: ByteReader) -> 'MaterialProperty':
        prop_name = reader.read_str()
        prop_type = reader.read_int()

        match prop_type:
            case 0:
                return MaterialPropertyColor(
                    name=prop_name,
                    color=reader.read_vec4()
                )
            case 1:
                return MaterialPropertyVector(
                    name=prop_name,
                    value=reader.read_vec4()
                )
            case 2:
                return MaterialPropertyFloat2(
                    name=prop_name,
                    value=reader.read_float()
                )
            case 3:
                return MaterialPropertyFloat3(
                    name=prop_name,
                    value=reader.read_float()
                )
            case 4:
                return MaterialPropertyTexture(
                    name=prop_name,
                    texture_index=reader.read_int(),
                    scale=reader.read_vec2(),
                    offset=reader.read_vec2()
                )

        raise Exception(f"Unknown material property with type id: {prop_type}")


class MaterialPropertyColor(MaterialProperty):
    def __init__(self, name: str, color: Vec4):
        super().__init__(name)

        self.color = color

    def write_base(self, writer: ByteWriter):
        writer.write_str(self.name)
        writer.write_int(0)
        writer.write_vec4(self.color)


class MaterialPropertyVector(MaterialProperty):
    def __init__(self, name: str, value: Vec4):
        super().__init__(name)

        self.value = value

    def write_base(self, writer: ByteWriter):
        writer.write_str(self.name)
        writer.write_int(1)
        writer.write_vec4(self.value)


class MaterialPropertyFloat2(MaterialProperty):
    def __init__(self, name: str, value: float):
        super().__init__(name)

        self.value = value

    def write_base(self, writer: ByteWriter):
        writer.write_str(self.name)
        writer.write_int(2)
        writer.write_float(self.value)


class MaterialPropertyFloat3(MaterialProperty):
    def __init__(self, name: str, value: float):
        super().__init__(name)

        self.value = value

    def write_base(self, writer: ByteWriter):
        writer.write_str(self.name)
        writer.write_int(3)
        writer.write_float(self.value)


class MaterialPropertyTexture(MaterialProperty):
    def __init__(self, name: str, texture_index: int, scale: Vec2, offset: Vec2):
        super().__init__(name)

        self.texture_index = texture_index
        self.scale = scale
        self.offset = offset

    def write_base(self, writer: ByteWriter):
        writer.write_str(self.name)
        writer.write_int(4)
        writer.write_int(self.texture_index)
        writer.write_vec2(self.scale)
        writer.write_vec2(self.offset)
