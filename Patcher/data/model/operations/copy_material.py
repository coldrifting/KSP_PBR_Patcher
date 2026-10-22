from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from utils.exceptions import ArgumentException
from utils.yaml_load import get_yaml_parameter


class OperationCopyMaterial(Operation):
    def __init__(self, material: str, new_name: str, transforms: list[str]):
        self.material = material
        self.new_name = new_name
        self.transforms = transforms

    def apply(self, mu_data: MuData):
        mu_data.copy_material(self.material, self.new_name)
        for transform in self.transforms:
            mu_data.assign_material(transform, self.new_name)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationCopyMaterial':
        material: str = get_yaml_parameter(yaml, "material", str)

        new_name: str | None = yaml.get("new_name", None)
        if new_name is None:
            suffix: str | None = yaml.get("suffix")
            if suffix is None:
                raise ArgumentException("missing required parameter: new_name or suffix")

            new_name: str = material + "-" + suffix

        transforms = get_yaml_parameter(yaml, "transforms", list)

        return OperationCopyMaterial(
            material=material,
            new_name=new_name,
            transforms=transforms)
