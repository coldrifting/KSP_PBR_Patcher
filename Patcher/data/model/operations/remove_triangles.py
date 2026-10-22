from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from utils.string_to_range import string_to_range
from utils.yaml_load import get_yaml_parameter


class OperationRemoveTriangles(Operation):
    def __init__(self, transform: str, triangles: list[int]):
        self.transform = transform
        self.triangles = triangles

    def apply(self, mu_data: MuData):
        mu_data.remove_triangles(self.transform, self.triangles)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationRemoveTriangles':
        transform = get_yaml_parameter(yaml, "transform", str)

        triangles_range = get_yaml_parameter(yaml, "triangles", str)
        triangles = string_to_range(triangles_range)

        return OperationRemoveTriangles(
            transform=transform,
            triangles=triangles)
