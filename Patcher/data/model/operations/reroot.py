from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from data.model.types.transform import Transform
from utils.yaml_load import get_yaml_parameter


class OperationReroot(Operation):
    def __init__(self, name: str):
        self.name = name

    def apply(self, mu_data: MuData):
        subroot: Transform = Transform(self.name)

        root_children: list[Transform] = []
        for i in reversed(range(len(mu_data.root_transform.children))):
            root_children.append(mu_data.root_transform.children[i])
            del mu_data.root_transform.children[i]

        subroot.children = list(reversed(root_children))

        mu_data.root_transform.children.append(subroot)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationReroot':
        name = get_yaml_parameter(yaml, "name", str)

        return OperationReroot(name=name)
