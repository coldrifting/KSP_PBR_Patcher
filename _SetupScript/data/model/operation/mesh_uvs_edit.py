from typing import Any

from data.model.operation.base import ModelOperation
from data.model.types.core.vec2 import Vec2
from data.model.types.mu_file import MuFile


class ModelOperationMeshEditSetUvs(ModelOperation):
    def __init__(self, transform_name: str, uvs: dict[int, Vec2]):
        self.transform_name = transform_name
        self.uvs = uvs

    def apply(self, mu_data: MuFile):
        mesh = mu_data.get_mesh(self.transform_name)
        mesh_uvs = mesh.uvs()

        for key, value in self.uvs.items():
            mesh_uvs[key] = value

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'ModelOperationMeshEditSetUvs':
        uvs: dict[int, Vec2] = {}

        for index, vert in yaml['uvs'].items():
            uvs[index] = Vec2(**vert)

        return ModelOperationMeshEditSetUvs(
            transform_name = yaml['transform_name'],
            uvs = uvs
        )
