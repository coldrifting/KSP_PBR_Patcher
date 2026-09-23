from typing import Any

from data.model.operation.base import ModelOperation
from data.model.types.mu_file import MuFile


class ModelOperationTransformMerge(ModelOperation):
    def __init__(self, transform_name_primary: str, transform_name_secondary: str):
        self.transform_name_primary = transform_name_primary
        self.transform_name_secondary = transform_name_secondary

    def apply(self, mu_data: MuFile):
        mu_data.merge_transforms(self.transform_name_primary, self.transform_name_secondary)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'ModelOperationTransformMerge':
        return ModelOperationTransformMerge(
            transform_name_primary = yaml['transform_name_primary'],
            transform_name_secondary = yaml['transform_name_secondary']
        )