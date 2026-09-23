from typing import Any

from data.model.operation.base import ModelOperation
from data.model.types.mu_file import MuFile
from data.model.types.mu_transform import Transform
from utils.exceptions import AttributeInvalidError, AttributeNotFoundError


class ModelOperationTransformRemove(ModelOperation):
    def __init__(self, transform_name: str):
        self.transform_name = transform_name

    def apply(self, mu_data: MuFile):
        if len(mu_data.root_transform.children) == 0:
            raise AttributeInvalidError("Root transform has no children and can not be removed")

        if not remove(mu_data.root_transform.children, self.transform_name):
            raise AttributeNotFoundError(f"Transform with name {self.transform_name} not found")

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'ModelOperationTransformRemove':
        return ModelOperationTransformRemove(
            transform_name = yaml['transform_name']
        )

def remove(transforms: list[Transform], transform_name: str) -> bool:
    for i in range(len(transforms)):
        if transforms[i].name == transform_name:
            del transforms[i]
            return True

    for child in transforms:
        if len(child.children) > 0:
            if remove(child.children, transform_name):
                return True

    return False