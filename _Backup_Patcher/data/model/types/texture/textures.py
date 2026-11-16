from typing import Iterator

from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.texture.texture import Texture
from data.model.types.tag.tag_mu import MuTag
from utils.exceptions import ArgumentException, AttributeNotFoundError


class Textures:
    def __init__(self, textures: list[Texture]):
        self.textures = textures

    def __iter__(self) -> Iterator[Texture]:
        return iter(self.textures)

    def __getitem__(self, index_or_key: int | str) -> Texture:
        if isinstance(index_or_key, int):
            return self.textures[index_or_key]

        if isinstance(index_or_key, str):
            index = self.get_index(index_or_key)
            if index == -1:
                raise AttributeNotFoundError(f'Texture with name {index_or_key} not found in model')

            return self.textures[index]

        raise ValueError(f"{index_or_key} is an invalid texture accessor")

    def __len__(self) -> int:
        return len(self.textures)

    def __delitem__(self, key):
        del self.textures[key]

    def get_index(self, texture_name: str):
        for index, material in enumerate(self.textures):
            if material.name == texture_name:
                return index

        return -1

    @classmethod
    def read(cls, reader: ByteReader) -> 'Textures':
        try:
            tag_num = reader.read_int()
            tag: MuTag = MuTag(tag_num)
            if tag != MuTag.Textures:
                raise ArgumentException(f"Expected {MuTag.Textures} but got {tag}")

            textures: list[Texture] = []
            num_textures = reader.read_int()
            for i in range(num_textures):
                texture: Texture = Texture.read(reader)
                textures.append(texture)

            return cls(textures)

        except EOFError:
            return cls([])

    def write(self, writer: ByteWriter):
        if len(self.textures) == 0:
            return

        writer.write_tag(MuTag.Textures)

        writer.write_int(len(self.textures))
        for texture in self.textures:
            texture.write(writer)

    def append(self, texture: Texture):
        self.textures.append(texture)
