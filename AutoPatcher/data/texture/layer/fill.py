from io import BytesIO
from pathlib import Path
from typing import Any, Tuple

import cairosvg
from PIL import Image

from data.texture.layer.base import Layer
from utils.exceptions import ArgumentException


class Fill(Layer):
    def __init__(self,
                 color: str | None,
                 image: str | None,
                 channels: str,
                 masks: list[Tuple[str, bool]],
                 invert_masks: bool,
                 group_type: str):
        super().__init__(masks, invert_masks, group_type)

        self.color = color.lower() if isinstance(color, str) else color
        self.image = image
        self.channels = channels.lower() if isinstance(channels, str) else "rgba"

    def apply(self,
              size: Tuple[int, int],
              prev_channels: dict[str, Image.Image],
              image: Image.Image,
              config_path: Path,
              game_data: Path):
        is_png_fill = False
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
                image_path = Path(game_data / self.image)
            elif self.image.endswith(".png"):
                image_path = Path(config_path / "Fill" / self.image)
                is_png_fill = True
            elif self.image.endswith(".svg"):
                image_path = Path(config_path / "Masks" / self.image)
            else:
                raise ArgumentException(f"Invalid image type: {self.image}")

            if not image_path.exists():
                raise ArgumentException(f"The following image file was not found:\r\n"
                      f"{image_path}")

            if self.image.endswith(".svg"):
                layer_image = Image.open(BytesIO(cairosvg.svg2png(url=image_path)))
            else:
                layer_image = Image.open(image_path)

            if layer_image.mode != "RGBA":
                layer_image = layer_image.convert("RGBA")

            if self.channels == "a":
                a = layer_image.getchannel("A")
                layer_image = Image.merge("RGB", (a, a, a)).convert("RGBA")
            elif self.channels == "rgb":
                r, g, b, _ = layer_image.split()
                layer_image = Image.merge("RGB", (r, g, b)).convert("RGBA")

        custom_mask = None
        if len(self.masks) == 0 and is_png_fill:
            custom_mask = layer_image.getchannel("A")

        self.apply_mask(
            image=image,
            layer_image=layer_image,
            config_path=config_path,
            custom_mask=custom_mask
        )

    @staticmethod
    def from_yaml(yaml: dict[str, Any], masks: list[tuple[str, bool]], group_type: str) -> 'Fill':
        color = yaml.get("color", None)

        image = yaml.get("image", None)
        channels = yaml.get("channels", "")
        if channels == "":
            channels = "rgba"

        if image is None and color is None:
            raise ArgumentException("A fill layer can have either a color or an image set, not both\r\n" +
                  "Did you forget to wrap a hex color in quotes?")

        return Fill(
            color=color,
            image=image,
            channels=channels,
            masks=masks,
            invert_masks=yaml.get("invert_masks", False),
            group_type=group_type
        )
