from pathlib import Path
from typing import Any, Tuple

from PIL import Image

from data.texture.layer.base import Layer
from utils.exceptions import ArgumentException


class Copy(Layer):
    def __init__(self, group: str, masks: list[Tuple[str, bool]], invert_masks: bool, group_type: str):
        super().__init__(masks, invert_masks, group_type)

        self.group = group

    def apply(self,
              size: Tuple[int, int],
              prev_channels: dict[str, Image.Image],
              image: Image.Image,
              config_path: Path,
              game_data: Path):
        if prev_channels.get(self.group) is None:
            raise ArgumentException(f"Group {self.group} does not exist, or has not been created yet")

        layer_image = prev_channels[self.group].copy()

        self.apply_mask(
            image=image,
            layer_image=layer_image,
            config_path=config_path
        )

    @staticmethod
    def from_yaml(yaml: dict[str, Any], masks: list[tuple[str, bool]], group_type: str) -> 'Copy':
        group: str | None = yaml.get("group", None)
        if group is None:
            raise ArgumentException("Missing required parameter 'group' for effect copy")

        return Copy(
            group=group,
            masks=masks,
            invert_masks=yaml.get("invert_masks", False),
            group_type=group_type
        )
