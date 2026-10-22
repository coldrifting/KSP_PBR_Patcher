from pathlib import Path
from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from utils.yaml_load import get_yaml_parameter


class OperationEditMaterialTextures(Operation):
    def __init__(self,
                 material: str,
                 main_tex: str | None,
                 bump_map: str | None,
                 emissive: str | None,
                 metal_map: str | None,
                 team_color_map: str | None):
        self.material = material
        self.main_tex: Path | None = Path(main_tex) if main_tex is not None else None
        self.bump_map: Path | None = Path(bump_map) if bump_map is not None else None
        self.emissive: Path | None = Path(emissive) if emissive is not None else None
        self.metal_map: Path | None = Path(metal_map) if metal_map is not None else None
        self.team_color_map: Path | None = Path(team_color_map) if team_color_map is not None else None

    def apply(self, mu_data: MuData):
        if self.main_tex is not None:
            mu_data.split_texture(self.material, "_MainTex", self.main_tex.name)

        if self.bump_map is not None:
            mu_data.split_texture(self.material, "_BumpMap", self.bump_map.name)

        if self.emissive is not None:
            mu_data.split_texture(self.material, "_Emissive", self.emissive.name)

        if self.metal_map is not None:
            mu_data.split_texture(self.material, "_MetalMap", self.metal_map.name)

        if self.team_color_map is not None:
            mu_data.split_texture(self.material, "_TeamColorMap", self.team_color_map.name)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationEditMaterialTextures':
        material: str = get_yaml_parameter(yaml, "material", str)

        main_tex: str | None = yaml.get("main_tex", None)
        bump_map: str | None = yaml.get("bump_map", None)
        emissive: str | None = yaml.get("emissive", None)
        metal_map: str | None = yaml.get("metal_map", None)
        team_color_map: str | None = yaml.get("team_color_map", None)

        return OperationEditMaterialTextures(
            material=material,
            main_tex=main_tex,
            bump_map=bump_map,
            emissive=emissive,
            metal_map=metal_map,
            team_color_map=team_color_map)
