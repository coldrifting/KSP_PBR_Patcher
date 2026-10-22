from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from utils.yaml_load import get_yaml_parameter


class OperationAssignMaterial(Operation):
    def __init__(self, material: str, transforms: list[str]):
        self.material = material
        self.transforms = transforms

    def apply(self, mu_data: MuData):
        for transform in self.transforms:
            mu_data.assign_material(transform, self.material)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationAssignMaterial':
        material = get_yaml_parameter(yaml, "material", str)
        transforms = get_yaml_parameter(yaml, "transforms", list)

        return OperationAssignMaterial(
            material=material,
            transforms=transforms)
