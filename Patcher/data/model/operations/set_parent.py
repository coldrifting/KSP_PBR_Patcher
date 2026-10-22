from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from utils.yaml_load import get_yaml_parameter


class OperationSetParent(Operation):
    def __init__(self, parent: str, transforms: list[str]):
        self.parent = parent
        self.transforms = transforms

    def apply(self, mu_data: MuData):
        mu_data.set_parent(self.parent, self.transforms)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationSetParent':
        parent = get_yaml_parameter(yaml, "parent", str)
        transforms = get_yaml_parameter(yaml, "transforms", list)

        return OperationSetParent(
            parent=parent,
            transforms=transforms)
