from pathlib import Path
from typing import Any, Tuple
from xml.etree.ElementTree import Element

from PIL import Image

from data.model.types.core.int2 import Int2
from data.texture.layer import Layer
from data.texture.mask import Mask
from utils.exceptions import ArgumentException
from utils.yaml_load import get_yaml_parameter


class Tile(Layer):
    def __init__(self,
                 source: str,
                 top_left : Int2,
                 size : Int2,
                 scaled_size : Int2,
                 offset : Int2,
                 masks: list[Mask],
                 group_type: str):
        super().__init__(masks, group_type)

        self.source = source
        self.top_left = top_left
        self.size = size
        self.scaled_size = scaled_size
        self.offset = offset

    def apply(self,
              size: Tuple[int, int],
              prev_channels: dict[str, Image.Image],
              image: Image.Image,
              masks: dict[str, Element],
              fills: dict[str, Image.Image],
              game_data_dir: Path):
        image_path = Path(game_data_dir / self.source)
        if not image_path.exists():
            raise ArgumentException(f"Image file not found: \n{image_path}")

        source_image = Image.open(image_path)

        if not 0 <= self.top_left.x < source_image.width:
            raise ArgumentException(f"x coordinate out of range: \n{self.top_left.x}")

        if not 0 <= self.top_left.x + self.size.x < source_image.width:
            raise ArgumentException(f"x + width coordinate out of range: \n{self.top_left.x + self.size.x}")

        if not 0 <= self.top_left.y < source_image.height:
            raise ArgumentException(f"y coordinate out of range: \n{self.top_left.y}")

        if not 0 <= self.top_left.y + self.size.y < source_image.height:
            raise ArgumentException(f"y + height coordinate out of range: \n{self.top_left.y + self.size.y}")

        cropped = source_image.crop((self.top_left.x, self.top_left.y, self.top_left.x + self.size.x, self.top_left.y + self.size.y))

        if self.scaled_size.x != source_image.width or self.scaled_size.y != source_image.height:
            cropped = cropped.resize((self.scaled_size.x, self.scaled_size.y))

        layer_image = Image.new("RGB", size)
        for x in range(0, size[0], cropped.width):
            for y in range(0, size[1], cropped.height):
                layer_image.paste(cropped, (x, y))

        self.apply_mask(
            image=image,
            layer_image=layer_image,
            masks=masks
        )

    @staticmethod
    def from_yaml(yaml: dict[str, Any], masks: list[Mask], group_type: str) -> 'Tile':
        source: str = get_yaml_parameter(yaml, "source", str)

        top_left_yaml: dict[str, Any] | None = yaml.get("top_left", None)
        if top_left_yaml is None:
            raise ArgumentException("Invalid value for parameter top_left")

        top_left: Int2 = Int2.from_yaml(top_left_yaml)

        size_yaml: dict[str, Any] | None = yaml.get("size", None)
        if size_yaml is None:
            raise ArgumentException("Invalid value for parameter size")

        size: Int2 = Int2.from_yaml(size_yaml)

        scaled_size_yaml: dict[str, Any] | None = yaml.get("scaled_size", None)
        if scaled_size_yaml is None:
            scaled_size = Int2(size.x, size.y)
        else:
            scaled_size: Int2 = Int2.from_yaml(scaled_size_yaml)

        offset_yaml: dict[str, Any] | None = yaml.get("offset", None)
        if offset_yaml is None:
            offset = Int2(0, 0)
        else:
            offset: Int2 = Int2.from_yaml(offset_yaml)

        return Tile(
            source=source,
            top_left=top_left,
            size=size,
            scaled_size=scaled_size,
            offset=offset,
            masks=masks,
            group_type=group_type
        )
