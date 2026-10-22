from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from utils.string_to_range import string_to_range
from utils.yaml_load import get_yaml_parameter


class OperationCopyTriangles(Operation):
    def __init__(self, transform: str, triangles: list[int]):
        self.transform = transform
        self.triangles = triangles

    def apply(self, mu_data: MuData):
        mu_data.copy_triangles(self.transform, None, self.triangles)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationCopyTriangles':
        transform = get_yaml_parameter(yaml, "transform", str)

        triangles_range = get_yaml_parameter(yaml, "triangles", str)
        triangles = string_to_range(triangles_range)

        return OperationCopyTriangles(
            transform=transform,
            triangles=triangles)
