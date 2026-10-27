from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from utils.yaml_load import get_yaml_parameter


class OperationRenameMaterial(Operation):
    def __init__(self, material: str, new_name: str):
        self.material = material
        self.new_name = new_name

    def apply(self, mu_data: MuData):
        mu_data.materials[self.material].name = self.new_name

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationRenameMaterial':
        material = get_yaml_parameter(yaml, "material", str)
        new_name = get_yaml_parameter(yaml, "new_name", str)

        return OperationRenameMaterial(
            material=material,
            new_name=new_name)
