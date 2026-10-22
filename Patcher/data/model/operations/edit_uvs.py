from typing import Any

from data.model.types.core.vec2 import Vec2
from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from utils.exceptions import ArgumentException
from utils.yaml_load import get_yaml_parameter


class OperationEditUvs(Operation):
    def __init__(self, transform: str, uvs: dict[int, Vec2]):
        self.transform = transform
        self.uvs = uvs

    def apply(self, mu_data: MuData):
        mu_data.edit_uvs(self.transform, self.uvs, is_uv2=False)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationEditUvs':
        transform = get_yaml_parameter(yaml, "transform", str)

        uvs_yaml = yaml.get("uvs", None)
        if uvs_yaml is None:
            raise ArgumentException("Missing required parameter uvs")

        if not isinstance(uvs_yaml, dict):
            raise ArgumentException("Invalid parameter uvs")

        uvs: dict[int, Vec2] = {}
        for index, uv in uvs_yaml.items():
            uvs[index] = Vec2.from_yaml(uv)

        return OperationEditUvs(transform, uvs)
