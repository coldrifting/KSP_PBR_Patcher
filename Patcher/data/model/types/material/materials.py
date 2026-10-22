from typing import Iterator

from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.material.material import Material
from data.model.types.tag.tag_mu import MuTag
from utils.exceptions import ArgumentException, AttributeNotFoundError


class Materials:
    def __init__(self, materials: list[Material]):
        self.materials = materials

    def __iter__(self) -> Iterator[Material]:
        return iter(self.materials)

    def __getitem__(self, index_or_key: int | str) -> Material:
        if isinstance(index_or_key, int):
            return self.materials[index_or_key]

        if isinstance(index_or_key, str):
            index = self.get_index(index_or_key)
            if index == -1:
                raise AttributeNotFoundError(f'Material with name {index_or_key} not found in model')

            return self.materials[index]

        raise ValueError(f"{index_or_key} is an invalid material accessor")

    def __len__(self) -> int:
        return len(self.materials)

    def __delitem__(self, key):
        del self.materials[key]

    def get_index(self, material_name: str):
        for index, material in enumerate(self.materials):
            if material.name == material_name:
                return index

        return -1

    @classmethod
    def read(cls, reader: ByteReader) -> 'Materials':
        try:
            tag_num = reader.read_int()
            tag: MuTag = MuTag(tag_num)
            if tag != MuTag.Materials:
                raise ArgumentException(f"Expected {MuTag.Materials} but got {tag}")

            materials: list[Material] = []
            num_materials = reader.read_int()
            for i in range(num_materials):
                material: Material = Material.read(reader)
                materials.append(material)

            return cls(materials)

        except EOFError:
            return cls([])

    def write(self, writer: ByteWriter):
        if len(self.materials) == 0:
            return

        writer.write_tag(MuTag.Materials)

        writer.write_int(len(self.materials))
        for material in self.materials:
            material.write(writer)

    def append(self, material: Material):
        self.materials.append(material)
