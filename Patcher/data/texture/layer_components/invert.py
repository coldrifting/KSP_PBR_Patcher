from pathlib import Path
from typing import Any, Tuple
from xml.etree.ElementTree import Element

from PIL import Image, ImageOps

from data.texture.layer import Layer
from data.texture.mask import Mask


class Invert(Layer):
    def __init__(self,
                 masks: list[Mask],
                 group_type: str):
        super().__init__(masks, group_type)

    def apply(self,
              size: Tuple[int, int],
              prev_channels: dict[str, Image.Image],
              image: Image.Image,
              masks: dict[str, Element],
              fills: dict[str, Image.Image],
              game_data_dir: Path):
        layer_image = ImageOps.invert(image)

        self.apply_mask(
            image=image,
            layer_image=layer_image,
            masks=masks
        )

    @staticmethod
    def from_yaml(yaml: dict[str, Any], masks: list[Mask], group_type: str) -> 'Invert':
        return Invert(
            masks=masks,
            group_type=group_type
        )
