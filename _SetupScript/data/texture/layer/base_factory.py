from typing import Any

from data.texture.layer.base import Layer
from data.texture.layer.brightness import Brightness
from data.texture.layer.copy import Copy
from data.texture.layer.curves import Curves
from data.texture.layer.fill import Fill
from data.texture.layer.invert import Invert
from data.texture.layer.saturation import Saturation
from utils.exceptions import AttributeInvalidError


class LayerFactory:
    @staticmethod
    def from_yaml(yaml: dict[str, Any], group_type) -> Layer:
        layer_type = list(yaml.keys())[0]
        yaml_layer = yaml[layer_type]

        if yaml_layer is None:
            raise AttributeInvalidError("Unable to create layer. Did you forget an indent?\n"
                                        f"{yaml}")

        yaml_masks: str | list[str] = yaml_layer.get("masks", None)
        if yaml_masks is None:
            yaml_mask = yaml_layer.get("mask", None)
            yaml_masks = [yaml_mask] if yaml_mask is not None else []

        if isinstance(yaml_masks, str):
            yaml_masks = [yaml_masks]

        masks = []
        for mask in yaml_masks:
            if mask.endswith("!"):
                mask = (mask[:-1], True)
            else:
                mask = (mask, False)
            masks.append(mask)

        match layer_type:
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
            case "saturation":
                return Saturation.from_yaml(yaml_layer, masks, group_type)
            case _:
                raise NotImplementedError
