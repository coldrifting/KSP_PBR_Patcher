from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from data.model.types.transform import Transform
from utils.exceptions import ArgumentException
from utils.yaml_load import get_yaml_parameter


class OperationRenameTransform(Operation):
    def __init__(self, transform: str, new_name: str):
        self.transform = transform
        self.new_name = new_name

    def apply(self, mu_data: MuData):
        transforms: list[Transform] = mu_data.get_transforms(self.transform, None)
        if len(transforms) == 0:
            raise ArgumentException(f"No transforms found with the name {self.transform}")

        for transform in transforms:
            transform.name = self.new_name

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationRenameTransform':
        transform = get_yaml_parameter(yaml, "transform", str)
        new_name = get_yaml_parameter(yaml, "new_name", str)

        return OperationRenameTransform(transform=transform,
                                        new_name=new_name)
