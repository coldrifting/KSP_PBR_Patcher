from xml.etree.ElementTree import Element
from pathlib import Path
from typing import Any, Tuple

from PIL import Image

from data.texture.layer import Layer
from data.texture.mask import Mask
from utils.exceptions import ArgumentException


class Fill(Layer):
    def __init__(self,
                 color: str | None,
                 image: str | None,
                 channels: str,
                 masks: list[Mask],
                 group_type: str):
        super().__init__(masks, group_type)

        self.color = color.lower() if isinstance(color, str) else color
        self.image = image
        self.channels = channels.lower() if isinstance(channels, str) else "rgba"

    def apply(self,
              size: Tuple[int, int],
              prev_channels: dict[str, Image.Image],
              image: Image.Image,
              masks: dict[str, Element],
              fills: dict[str, Image.Image],
              game_data_dir: Path):
        if self.color is not None:
            if self.color.startswith("#"):
                hex_string: str = self.color.lstrip("#").rstrip()
                if len(hex_string) != 6:
                    raise ArgumentException("Invalid fill color: Hex code must be 6 characters long")

                r = int(hex_string[0:2], 16)
                g = int(hex_string[2:4], 16)
                b = int(hex_string[4:6], 16)

                color = (r, g, b, 255)
            elif self.color == "white":
                color = (255, 255, 255, 255)
            elif self.color == "black":
                color = (0, 0, 0, 255)
            else:
                raise ArgumentException("Invalid fill color: Unknown color")

            layer_image = Image.new("RGBA", size, color)
        else:
            if self.image is None:
                raise ArgumentException("Image should not be None")

            if self.image.endswith(".dds"):
                image_path = Path(game_data_dir / self.image)
                if not image_path.exists():
                    raise ArgumentException(f"Image file not found: \n{image_path}")

                layer_image = Image.open(image_path)
            else:
                layer_image = fills.get(self.image, None)
                if layer_image is None:
                    raise ArgumentException(f"Image not found in svg file: \n{self.image}")

            if layer_image.mode != "RGBA":
                layer_image = layer_image.convert("RGBA")

            if self.channels == "a":
                a = layer_image.getchannel("A")
                layer_image = Image.merge("RGB", (a, a, a)).convert("RGBA")
            elif self.channels == "rgb":
                r, g, b, _ = layer_image.split()
                layer_image = Image.merge("RGB", (r, g, b)).convert("RGBA")

        custom_mask = None
        if len(self.masks) == 0:
            custom_mask = layer_image.getchannel("A")

        self.apply_mask(
            image=image,
            layer_image=layer_image,
            masks=masks,
            custom_mask=custom_mask
        )

    @staticmethod
    def from_yaml(yaml: dict[str, Any], masks: list[Mask], group_type: str) -> 'Fill':
        color = yaml.get("color", None)

        image = yaml.get("image", None)
        channels = yaml.get("channels", "")
        if channels == "":
            channels = "rgba"

        if image is None and color is None:
            raise ArgumentException("A fill layer_components can have either a color or an image set, not both\r\n" +
                  "Did you forget to wrap a hex color in quotes?")

        return Fill(
            color=color,
            image=image,
            channels=channels,
            masks=masks,
            group_type=group_type
        )
