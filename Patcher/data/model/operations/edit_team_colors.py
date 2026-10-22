from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from utils.team_color import TeamColor
from utils.yaml_load import get_yaml_parameter


class OperationEditTeamColors(Operation):
    def __init__(self, material: str, tc1: str, tc2: str | None):
        self.material = material
        self.tc1 = tc1
        self.tc2 = tc2

    def apply(self, mu_data: MuData):
        tc1, tc2 = TeamColor.get_colors(self.tc1, self.tc2)
        mu_data.assign_team_colors(self.material, tc1, tc2)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationEditTeamColors':
        material = get_yaml_parameter(yaml, "material", str)
        tc1 = get_yaml_parameter(yaml, "tc1", str)
        tc2 = yaml.get("tc2", None)

        return OperationEditTeamColors(
            material=material,
            tc1=tc1,
            tc2=tc2)
