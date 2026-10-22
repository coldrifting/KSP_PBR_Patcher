from typing import Any

from data.model.types.core.vec3 import Vec3
from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from utils.exceptions import ArgumentException
from utils.yaml_load import get_yaml_parameter


class OperationEditNormals(Operation):
    def __init__(self, transform: str, normals: dict[int, Vec3]):
        self.transform = transform
        self.normals = normals

    def apply(self, mu_data: MuData):
        mu_data.edit_normals(self.transform, self.normals)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationEditNormals':
        transform = get_yaml_parameter(yaml, "transform", str)

        normals_yaml = yaml.get("normals", None)
        if normals_yaml is None:
            raise ArgumentException("Missing required parameter normals")

        if not isinstance(normals_yaml, dict):
            raise ArgumentException("Invalid parameter normals")

        normals: dict[int, Vec3] = {}
        for index, normal in normals_yaml.items():
            normals[index] = Vec3.from_yaml(normal)

        return OperationEditNormals(transform, normals)
