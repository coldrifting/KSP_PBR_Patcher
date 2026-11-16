from pathlib import Path
from typing import Any, Tuple
from xml.etree.ElementTree import Element

from PIL import Image, ImageFilter

from data.texture.layer import Layer
from data.texture.mask import Mask
from utils.exceptions import ArgumentException


class Blur(Layer):
    def __init__(self,
                 radius: float | int,
                 masks: list[Mask],
                 group_type: str):
        super().__init__(masks, group_type)

        self.radius = radius

    def apply(self,
              size: Tuple[int, int],
              prev_channels: dict[str, Image.Image],
              image: Image.Image,
              masks: dict[str, Element],
              fills: dict[str, Image.Image],
              game_data_dir: Path):

        layer_image = image.filter(ImageFilter.GaussianBlur(self.radius))

        self.apply_mask(
            image=image,
            layer_image=layer_image,
            masks=masks
        )

    @staticmethod
    def from_yaml(yaml: dict[str, Any], masks: list[Mask], group_type: str) -> 'Blur':
        radius: float | int | None = yaml.get("radius", None)
        if radius is None:
            raise ArgumentException("Missing required parameter 'radius' for effect blur")

        return Blur(
            radius=radius,
            masks=masks,
            group_type=group_type
        )
