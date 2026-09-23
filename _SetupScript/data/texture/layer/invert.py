from pathlib import Path
from typing import Any, Tuple

from PIL import Image, ImageOps

from data.texture.layer.base import Layer


class Invert(Layer):
    def __init__(self, masks: list[Tuple[str, bool]], invert_masks: bool, group_type: str):
        super().__init__(masks, invert_masks, group_type)

    def apply(self,
              size: Tuple[int, int],
              prev_channels: dict[str, Image.Image],
              image: Image.Image,
              config_path: Path,
              game_data: Path):
        layer_image = ImageOps.invert(image)

        self.apply_mask(
            image=image,
            layer_image=layer_image,
            config_path=config_path
        )

    @staticmethod
    def from_yaml(yaml: dict[str, Any], masks: list[tuple[str, bool]], group_type: str) -> 'Invert':
        return Invert(
            masks=masks,
            invert_masks=yaml.get("invert_masks", False),
            group_type=group_type
        )
