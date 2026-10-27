from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from data.model.operations.rotate_transform import OperationRotateTransform
from data.model.operations.scale_transform import OperationScaleTransform
from data.model.types.core.vec3 import Vec3
from utils.yaml_load import get_yaml_parameter


class OperationSetParent(Operation):
    def __init__(self, parent: str, transforms: list[str], reset_rot_and_scale: bool):
        self.parent = parent
        self.transforms = transforms
        self.reset_rot_and_scale = reset_rot_and_scale

    def apply(self, mu_data: MuData):
        mu_data.set_parent(self.parent, self.transforms)
        if self.reset_rot_and_scale:
            for transform in self.transforms:
                scale_operation = OperationScaleTransform(transform, 1.0, True)
                rotate_operation = OperationRotateTransform(transform, Vec3(0, 0, 0), True)

                scale_operation.apply(mu_data)
                rotate_operation.apply(mu_data)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationSetParent':
        parent = get_yaml_parameter(yaml, "parent", str)
        transforms = get_yaml_parameter(yaml, "transforms", list)
        reset_rot_and_scale = yaml.get("reset_rot_and_scale", True)

        return OperationSetParent(
            parent=parent,
            transforms=transforms,
            reset_rot_and_scale=reset_rot_and_scale)
