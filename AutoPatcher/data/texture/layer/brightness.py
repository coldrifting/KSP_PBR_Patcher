from pathlib import Path
from typing import Any, Tuple

from PIL import Image, ImageEnhance

from data.texture.layer.base import Layer
from utils.exceptions import ArgumentException


class Brightness(Layer):
    def __init__(self, percent: float | int, masks: list[Tuple[str, bool]], invert_masks: bool, group_type: str):
        super().__init__(masks, invert_masks, group_type)

        self.percent = percent

    def apply(self,
              size: Tuple[int, int],
              prev_channels: dict[str, Image.Image],
              image: Image.Image,
              config_path: Path,
              game_data: Path):
        enhancer = ImageEnhance.Brightness(image)
        layer_image = enhancer.enhance(self.percent / 100.0)

        self.apply_mask(
            image=image,
            layer_image=layer_image,
            config_path=config_path
        )

    @staticmethod
    def from_yaml(yaml: dict[str, Any], masks: list[tuple[str, bool]], group_type: str) -> 'Brightness':
        percent: float | int | None = yaml.get("percent", None)
        if percent is None:
            raise ArgumentException("Missing required parameter 'percent' for effect brightness")

        return Brightness(
            percent=percent,
            masks=masks,
            invert_masks=yaml.get("invert_masks", False),
            group_type=group_type
        )
