from typing import Any

from data.model.operation.base import ModelOperation
from data.model.types.core.vec3 import Vec3
from data.model.types.mu_file import MuFile


class ModelOperationMeshEditSetVertices(ModelOperation):
    def __init__(self, transform_name: str, vertices: dict[int, Vec3]):
        self.transform_name = transform_name
        self.vertices = vertices

    def apply(self, mu_data: MuFile):
        mesh = mu_data.get_mesh(self.transform_name)
        mesh_vertices = mesh.vertices()

        for key, value in self.vertices.items():
            mesh_vertices[key] = value

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'ModelOperationMeshEditSetVertices':
        vertices: dict[int, Vec3] = {}

        for index, vert in yaml['vertices'].items():
            vertices[index] = Vec3(**vert)

        return ModelOperationMeshEditSetVertices(
            transform_name = yaml['transform_name'],
            vertices = vertices
        )
