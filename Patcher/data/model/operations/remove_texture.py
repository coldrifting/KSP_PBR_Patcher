from pathlib import Path
from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from utils.exceptions import ArgumentException
from utils.yaml_load import get_yaml_parameter


class OperationRemoveTexture(Operation):
    def __init__(self, texture: str):
        self.texture = texture

    def apply(self, mu_data: MuData):
        for texture in mu_data.textures:
            if str(Path(texture.name).with_suffix("")) == str(Path(self.texture).with_suffix("")):
                mu_data.remove_texture(texture.name)
                return

        raise ArgumentException(f"Texture {self.texture} not found in model")


    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationRemoveTexture':
        texture = get_yaml_parameter(yaml, "texture", str)

        return OperationRemoveTexture(texture=texture)
