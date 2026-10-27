from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from data.model.types.core.vec3 import Vec3
from data.model.types.transform import Transform
from utils.exceptions import ArgumentException
from utils.yaml_load import get_yaml_parameter


class OperationScaleTransform(Operation):
    def __init__(self, transform: str, amount: Vec3 | float | int, absolute: bool):
        self.transform = transform
        self.amount = amount if isinstance(amount, Vec3) else Vec3(amount, amount, amount)
        self.absolute = absolute

    def apply(self, mu_data: MuData):
        transforms: list[Transform] = mu_data.get_transforms(self.transform, None)
        if len(transforms) == 0:
            raise ArgumentException(f"No transforms found with the name {self.transform}")

        for transform in transforms:
            if self.absolute:
                transform.scale = self.amount
            else:
                transform.scale *= self.amount

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationScaleTransform':
        transform = get_yaml_parameter(yaml, "transform", str)
        amount = yaml.get("amount", 1.0)
        absolute: bool = yaml.get("absolute", False)

        return OperationScaleTransform(
            transform=transform,
            amount=amount,
            absolute=absolute)
