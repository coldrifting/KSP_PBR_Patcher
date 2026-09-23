from typing import Any

from data.model.operation.base import ModelOperation
from data.model.types.mu_file import MuFile


class ModelOperationTransformDuplicate(ModelOperation):
    def __init__(self, transform_name: str, new_transform_name: str, clear_mesh_data: bool = False):
        self.transform_name = transform_name
        self.new_transform_name = new_transform_name
        self.clear_mesh_data = clear_mesh_data

    def apply(self, mu_data: MuFile):
        mu_data.clone_transform(
            self.transform_name,
            self.new_transform_name,
            self.clear_mesh_data
        )

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'ModelOperationTransformDuplicate':
        return ModelOperationTransformDuplicate(
            transform_name = yaml['transform_name'],
            new_transform_name = yaml['new_transform_name']
        )