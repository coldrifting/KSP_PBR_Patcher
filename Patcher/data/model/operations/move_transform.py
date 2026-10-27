from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from data.model.types.core.vec3 import Vec3
from data.model.types.transform import Transform
from utils.exceptions import ArgumentException
from utils.yaml_load import get_yaml_parameter


class OperationMoveTransform(Operation):
    def __init__(self, transform: str, amount: Vec3, absolute: bool):
        self.transform = transform
        self.amount = amount
        self.absolute = absolute

    def apply(self, mu_data: MuData):
        transforms: list[Transform] = mu_data.get_transforms(self.transform, None)
        if len(transforms) == 0:
            raise ArgumentException(f"No transforms found with the name {self.transform}")

        for transform in transforms:
            transform_position = Vec3(0, 0, 0) if self.absolute else transform.position
            new_position = transform_position + self.amount
            transform.position = new_position

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationMoveTransform':
        transform = get_yaml_parameter(yaml, "transform", str)
        amount_yaml: dict[str, Any] | None = yaml.get("amount", None)
        if amount_yaml is None:
            raise ArgumentException(f"Missing or invalid parameter amount for operation move_transform")

        amount = Vec3.from_yaml(amount_yaml)
        absolute: bool = yaml.get("absolute", False)

        return OperationMoveTransform(
            transform=transform,
            amount=amount,
            absolute=absolute)
