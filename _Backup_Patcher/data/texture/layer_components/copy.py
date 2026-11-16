from pathlib import Path
from typing import Any, Tuple
from xml.etree.ElementTree import Element

from PIL import Image

from data.texture.layer import Layer
from data.texture.mask import Mask
from utils.exceptions import ArgumentException


class Copy(Layer):
    def __init__(self,
                 group: str,
                 masks: list[Mask],
                 group_type: str):
        super().__init__(masks, group_type)

        self.group = group

    def apply(self,
              size: Tuple[int, int],
              prev_channels: dict[str, Image.Image],
              image: Image.Image,
              masks: dict[str, Element],
              fills: dict[str, Image.Image],
              game_data_dir: Path):
        if prev_channels.get(self.group) is None:
            raise ArgumentException(f"Group {self.group} does not exist, or has not been created yet")

        layer_image = prev_channels[self.group].copy()

        self.apply_mask(
            image=image,
            layer_image=layer_image,
            masks=masks
        )

    @staticmethod
    def from_yaml(yaml: dict[str, Any], masks: list[Mask], group_type: str) -> 'Copy':
        group: str | None = yaml.get("group", None)
        if group is None:
            raise ArgumentException("Missing required parameter 'group' for effect copy")

        return Copy(
            group=group,
            masks=masks,
            group_type=group_type
        )
