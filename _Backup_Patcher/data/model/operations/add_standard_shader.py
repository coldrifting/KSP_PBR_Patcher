from pathlib import Path
from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from utils.yaml_load import get_yaml_parameter


class OperationAddStandardShader(Operation):
    def __init__(self, material: str):
        self.material = material

    def apply(self, mu_data: MuData, game_data_dir: Path):
        mu_data.assign_resurfaced_standard_shader(self.material)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationAddStandardShader':
        material = get_yaml_parameter(yaml, "material", str)

        return OperationAddStandardShader(
            material=material)
