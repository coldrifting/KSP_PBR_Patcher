from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from utils.yaml_load import get_yaml_parameter


class OperationRemoveTransform(Operation):
    def __init__(self, transform: str):
        self.transform = transform

    def apply(self, mu_data: MuData):
        mu_data.remove_transform(self.transform)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationRemoveTransform':
        transform = get_yaml_parameter(yaml, "transform", str)

        return OperationRemoveTransform(transform=transform)
