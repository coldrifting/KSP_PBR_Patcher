from pathlib import Path
from typing import Tuple
from xml.etree.ElementTree import Element

from PIL import Image, ImageOps

from data.texture.mask import Mask
from utils.exceptions import ArgumentException
from utils.svg_split import new_svg, recolor_element, get_image


class Layer:
    def __init__(self,
                 masks: list[Mask],
                 group_type: str):
        self.group_type = group_type
        self.masks = masks

    def __str__(self):
        return f"Layer [{type(self).__name__}] ({self.group_type})"

    def apply_mask(self,
                   image: Image.Image,
                   layer_image: Image.Image,
                   masks: dict[str, Element],
                   custom_mask: Image.Image | None = None):
        if len(self.masks) == 0:
            image.paste(layer_image, None, custom_mask)
            return

        if self.masks[0].name == "bg":
            mask_svg = new_svg(layer_image.size, self.masks[0].color)
        else:
            mask_svg = new_svg(layer_image.size, "#000000")

        for index, mask in enumerate(self.masks):
            if index == 0 and mask.name == "bg":
                continue

            mask_svg_layer = masks.get(mask.name, None)
            if mask_svg_layer is None:
                raise ArgumentException(f"Mask {mask.name} was not found in svg file")

            recolor_element(mask_svg_layer, mask.color)
            mask_svg.append(mask_svg_layer)

        mask_image = get_image(mask_svg).convert('L')

        if custom_mask is not None:
            mask_image.paste(custom_mask, None, custom_mask)

        image.paste(layer_image, None, mask_image)

    def apply(self,
              size: Tuple[int, int],
              prev_channels: dict[str, Image.Image],
              image: Image.Image,
              masks: dict[str, Element],
              fills: dict[str, Image.Image],
              game_data_dir: Path):
        raise NotImplementedError(f"Not implemented for type {type(self).__name__}")
