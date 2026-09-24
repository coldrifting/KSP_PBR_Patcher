from pathlib import Path
from typing import Any, Tuple

from PIL import Image, ImageFilter

from data.texture.layer.base import Layer
from utils.exceptions import ArgumentException


class Blur(Layer):
    def __init__(self, radius: float | int, masks: list[Tuple[str, bool]], invert_masks: bool, group_type: str):
        super().__init__(masks, invert_masks, group_type)

        self.radius = radius

    def apply(self,
              size: Tuple[int, int],
              prev_channels: dict[str, Image.Image],
              image: Image.Image,
              config_path: Path,
              game_data: Path):

        layer_image = image.filter(ImageFilter.GaussianBlur(self.radius))

        self.apply_mask(
            image=image,
            layer_image=layer_image,
            config_path=config_path
        )

    @staticmethod
    def from_yaml(yaml: dict[str, Any], masks: list[tuple[str, bool]], group_type: str) -> 'Blur':
        radius: float | int | None = yaml.get("radius", None)
        if radius is None:
            raise ArgumentException("Missing required parameter 'radius' for effect blur")

        return Blur(
            radius=radius,
            masks=masks,
            invert_masks=yaml.get("invert_masks", False),
            group_type=group_type
        )
