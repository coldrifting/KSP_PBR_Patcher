from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from utils.exceptions import ArgumentException
from utils.yaml_load import get_yaml_parameter


class OperationEditNormalsAverage(Operation):
    def __init__(self, transform: str, vertex_groups: list[list[int]]):
        self.transform = transform
        self.vertex_groups = vertex_groups

    def apply(self, mu_data: MuData):
        mu_data.edit_normals_average(self.transform, self.vertex_groups)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationEditNormalsAverage':
        transform = get_yaml_parameter(yaml, "transform", str)

        vertex_groups: list[list[int]] | None = yaml.get("vertex_groups", None)
        if vertex_groups is None:
            raise ArgumentException("Missing requir ed parameter vertex_groups")

        return OperationEditNormalsAverage(
            transform=transform,
            vertex_groups=vertex_groups
        )
