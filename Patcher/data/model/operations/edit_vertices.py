from typing import Any

from data.model.types.core.vec3 import Vec3
from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from utils.exceptions import ArgumentException
from utils.yaml_load import get_yaml_parameter


class OperationEditVertices(Operation):
    def __init__(self, transform: str, vertices: dict[int, Vec3]):
        self.transform = transform
        self.vertices = vertices

    def apply(self, mu_data: MuData):
        mu_data.edit_vertices(self.transform, self.vertices)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationEditVertices':
        transform = get_yaml_parameter(yaml, "transform", str)

        verts_yaml = yaml.get("vertices", None)
        if verts_yaml is None:
            raise ArgumentException("Missing required parameter vertices")

        if not isinstance(verts_yaml, dict):
            raise ArgumentException("Invalid parameter vertices")

        vertices: dict[int, Vec3] = {}
        for index, vertex in verts_yaml.items():
            vertices[index] = Vec3.from_yaml(vertex)

        return OperationEditVertices(transform, vertices)
