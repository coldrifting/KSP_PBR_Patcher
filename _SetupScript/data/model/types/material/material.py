from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.material.material_property import MaterialProperty


class Material:
    def __init__(self, name: str, shader_name: str, properties: list[MaterialProperty]):
        self.name = name
        self.shader_name = shader_name
        self.properties = properties

    def __str__(self) -> str:
        return self.name

    def write(self, writer: ByteWriter):
        writer.write_str(self.name)
        writer.write_str(self.shader_name)
        writer.write_int(len(self.properties))
        for prop in self.properties:
            prop.write(writer)

    @staticmethod
    def read(reader: ByteReader) -> 'Material':
        name = reader.read_str()
        shader_name = reader.read_str()

        properties = []
        properties_count = reader.read_int()
        for i in range(properties_count):
            prop = MaterialProperty.read(reader)
            properties.append(prop)

        return Material(
            name = name,
            shader_name = shader_name,
            properties = properties
        )

    def clone(self, new_name: str):
        properties: list[MaterialProperty] = []

        for i in range(len(self.properties)):
            prop = self.properties[i].clone()
            properties.append(prop)

        return Material(new_name, self.shader_name, properties)