import errno
import os
from io import BytesIO
from pathlib import Path
from typing import Tuple

import cairosvg
from PIL import Image, ImageOps


class Layer:
    def __init__(self, masks: list[Tuple[str, bool]], invert_masks: bool, group_type: str):
        self.group_type = group_type
        self.masks = masks
        self.invert_masks = invert_masks

    def __str__(self):
        return f"Layer [{type(self).__name__}] ({self.group_type})"

    def apply_mask(self, image: Image.Image, layer_image: Image.Image, config_path: Path, custom_mask: Image.Image | None = None):
        if custom_mask is not None:
            image.paste(layer_image, None, custom_mask)
            return

        if len(self.masks) == 0:
            image.paste(layer_image, None, None)
            return

        mask_image = Image.new("RGBA", image.size, (0, 0, 0, 255))
        for mask in self.masks:
            mask_image_path = Path(config_path / "Masks" / Path(mask[0] + ".svg"))
            if not mask_image_path.exists():
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), mask_image_path)

            mask_image_as_png = Image.open(BytesIO(cairosvg.svg2png(url=mask_image_path)))
            if mask[1]:
                mask_image_as_png_inverted = ImageOps.invert(mask_image_as_png)
                mask_image.paste(mask_image_as_png_inverted, None, mask_image_as_png.getchannel("R"))
            else:
                mask_image.paste(mask_image_as_png, None, mask_image_as_png.getchannel("R"))

        mask_channel = mask_image.getchannel("R")
        mask_image = Image.merge("RGB", (mask_channel, mask_channel, mask_channel))

        if self.invert_masks:
            mask_image = ImageOps.invert(mask_image)

        mask_channel = mask_image.getchannel("R")
        mask_image = Image.merge("RGBA", (mask_channel, mask_channel, mask_channel, mask_channel))

        image.paste(layer_image, None, mask_image)

    def apply(self,
              size: Tuple[int, int],
              prev_channels: dict[str, Image.Image],
              image: Image.Image,
              config_path: Path,
              game_data: Path):
        raise NotImplementedError(f"Not implemented for type {type(self)}")
