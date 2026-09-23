from typing import Any

from data.model.operation.base import ModelOperation
from data.model.types.core.vec3 import Vec3
from data.model.types.mu_file import MuFile


class ModelOperationMeshEditAverageNormals(ModelOperation):
    def __init__(self, transform_name: str, vertex_groups: list[list[int]]):
        self.transform_name = transform_name
        self.vertex_groups = vertex_groups

    def apply(self, mu_data: MuFile):
        mesh = mu_data.get_mesh(self.transform_name)
        mesh_normals = mesh.normals()
        for i in range(len(self.vertex_groups)):
            sum_vec = Vec3(0,0,0)
            for j in range(len(self.vertex_groups[i])):
                sum_vec += mesh_normals[self.vertex_groups[i][j]]

            normalized = sum_vec.normalize()

            for j in range(len(self.vertex_groups[i])):
                mesh_normals[self.vertex_groups[i][j]] = normalized

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'ModelOperationMeshEditAverageNormals':
        return ModelOperationMeshEditAverageNormals(
            transform_name = yaml['transform_name'],
            vertex_groups = yaml['vertex_groups']
        )