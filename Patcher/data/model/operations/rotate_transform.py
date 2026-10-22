from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from data.model.types.core.vec3 import Vec3
from data.model.types.core.vec_utils import to_xyz_euler, to_quaternion
from data.model.types.transform import Transform
from utils.exceptions import ArgumentException
from utils.yaml_load import get_yaml_parameter


class OperationRotateTransform(Operation):
    def __init__(self, transform: str, amount: Vec3):
        self.transform = transform
        self.amount = amount

    def apply(self, mu_data: MuData):
        transforms: list[Transform] = mu_data.get_transforms(self.transform, None)
        if len(transforms) == 0:
            raise ArgumentException(f"No transforms found with the name {self.transform}")

        for transform in transforms:
            transform_rotation = to_xyz_euler(transform.rotation)
            new_rotation = (((transform_rotation + self.amount) + 360) % 720) - 360
            new_rotation_quaternion = to_quaternion(new_rotation)
            transform.rotation = new_rotation_quaternion

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationRotateTransform':
        transform = get_yaml_parameter(yaml, "transform", str)
        amount_yaml: dict[str, Any] | None = yaml.get("amount", None)
        if amount_yaml is None:
            raise ArgumentException(f"Missing or invalid parameter amount for operation rotate_transform")

        amount = Vec3.from_yaml(amount_yaml) % 360

        return OperationRotateTransform(
            transform=transform,
            amount=amount)
