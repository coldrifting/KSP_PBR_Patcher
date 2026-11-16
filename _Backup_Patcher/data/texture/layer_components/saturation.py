from pathlib import Path
from typing import Any, Tuple
from xml.etree.ElementTree import Element

from PIL import Image, ImageEnhance

from data.texture.layer import Layer
from data.texture.mask import Mask
from utils.exceptions import ArgumentException


class Saturation(Layer):
    def __init__(self,
                 percent: float | int,
                 masks: list[Mask],
                 group_type: str):
        super().__init__(masks, group_type)

        self.percent = percent

    def apply(self,
              size: Tuple[int, int],
              prev_channels: dict[str, Image.Image],
              image: Image.Image,
              masks: dict[str, Element],
              fills: dict[str, Image.Image],
              game_data_dir: Path):
        enhancer = ImageEnhance.Color(image)
        layer_image = enhancer.enhance(self.percent / 100.0)

        self.apply_mask(
            image=image,
            layer_image=layer_image,
            masks=masks
        )

    @staticmethod
    def from_yaml(yaml: dict[str, Any], masks: list[Mask], group_type: str) -> 'Saturation':
        percent: float | int | None = yaml.get("percent", None)
        if percent is None:
            raise ArgumentException("Missing required parameter 'percent' for effect saturation")

        return Saturation(
            percent=percent,
            masks=masks,
            group_type=group_type
        )
