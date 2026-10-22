from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from utils.yaml_load import get_yaml_parameter


class OperationCopyTransform(Operation):
    def __init__(self, transform: str, new_name: str):
        self.transform = transform
        self.new_name = new_name

    def apply(self, mu_data: MuData):
        mu_data.copy_transform(self.transform, self.new_name)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationCopyTransform':
        transform = get_yaml_parameter(yaml, "transform", str)
        new_name = get_yaml_parameter(yaml, "new_name", str)

        return OperationCopyTransform(
            transform=transform,
            new_name=new_name)
