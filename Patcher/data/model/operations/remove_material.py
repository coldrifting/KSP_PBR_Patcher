from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from utils.yaml_load import get_yaml_parameter


class OperationRemoveMaterial(Operation):
    def __init__(self, material: str):
        self.material = material

    def apply(self, mu_data: MuData):
        mu_data.remove_material(self.material)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationRemoveMaterial':
        material = get_yaml_parameter(yaml, "material", str)

        return OperationRemoveMaterial(material=material)
