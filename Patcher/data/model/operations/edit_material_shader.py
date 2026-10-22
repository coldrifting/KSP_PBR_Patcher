from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from utils.yaml_load import get_yaml_parameter


class OperationEditMaterialShader(Operation):
    def __init__(self, material: str, shader: str):
        self.material = material
        self.shader = shader

    def apply(self, mu_data: MuData):
        mu_data.edit_material_shader(self.material, self.shader)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationEditMaterialShader':
        material: str = get_yaml_parameter(yaml, "material", str)
        shader: str = get_yaml_parameter(yaml, "shader", str)

        return OperationEditMaterialShader(
            material=material,
            shader=shader)
