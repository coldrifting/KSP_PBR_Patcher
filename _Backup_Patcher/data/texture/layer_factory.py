from typing import Any

from data.texture.layer import Layer
from data.texture.layer_components.blur import Blur
from data.texture.layer_components.brightness import Brightness
from data.texture.layer_components.copy import Copy
from data.texture.layer_components.curves import Curves
from data.texture.layer_components.fill import Fill
from data.texture.layer_components.invert import Invert
from data.texture.layer_components.noise import Noise
from data.texture.layer_components.saturation import Saturation
from data.texture.layer_components.tile import Tile
from data.texture.mask import Mask
from utils.exceptions import AttributeInvalidError, ArgumentException


class LayerFactory:
    @staticmethod
    def from_yaml(yaml: dict[str, Any], group_type) -> Layer:
        layer_type = list(yaml.keys())[0]
        yaml_layer = yaml[layer_type]

        if yaml_layer is None:
            raise AttributeInvalidError("Unable to create layer_components. Did you forget an indent?\n{yaml}")

        yaml_masks: list[str] | None = yaml_layer.get("masks", [])
        if not isinstance(yaml_masks, list):
            raise AttributeInvalidError("Invalid type for parameter masks")

        if yaml_layer.get("mask"):
            raise AttributeInvalidError("Invalid parameter mask")

        if yaml_layer.get("invert_masks"):
            raise AttributeInvalidError("Invalid parameter invert_masks")

        masks: list[Mask] = []
        for yaml_mask in yaml_masks:
            if yaml_mask.endswith("!"):
                if yaml_mask[:-1] == "bg":
                    mask = Mask(yaml_mask[:-1], "#ffffff")
                else:
                    mask = Mask(yaml_mask[:-1], "#000000")
            elif "#" in yaml_mask:
                splits = yaml_mask.split("#")
                if len(splits) != 2:
                    raise ArgumentException(f"Invalid mask color format: {yaml_mask}")
                mask = Mask(splits[0], splits[1])
            else:
                mask = Mask(yaml_mask, "#ffffff")

            masks.append(mask)

        match layer_type:
            case "blur":
                return Blur.from_yaml(yaml_layer, masks, group_type)
            case "brightness":
                return Brightness.from_yaml(yaml_layer, masks, group_type)
            case "copy":
                return Copy.from_yaml(yaml_layer, masks, group_type)
            case "curves":
                return Curves.from_yaml(yaml_layer, masks, group_type)
            case "fill":
                return Fill.from_yaml(yaml_layer, masks, group_type)
            case "invert":
                return Invert.from_yaml(yaml_layer, masks, group_type)
            case "noise":
                return Noise.from_yaml(yaml_layer, masks, group_type)
            case "saturation":
                return Saturation.from_yaml(yaml_layer, masks, group_type)
            case "tile":
                return Tile.from_yaml(yaml_layer, masks, group_type)
            case _:
                raise NotImplementedError
