import copy
from typing import Any

from data.material.config_patch_part import ConfigPart
from data.material.material_def import ConfigPartMaterialDef
from utils.exceptions import ArgumentException

class ConfigPatch:
    def __init__(self,
                 materials: dict[str, ConfigPartMaterialDef],
                 parts: list[ConfigPart]):
        self.materials = materials
        self.parts = parts

    def write(self) -> str:
        output = "//// Materials\n"
        for material_name, material in self.materials.items():
            output += material.write()
            output += "\n"

        output += "//// Parts\n"
        count: int = 0
        for part in self.parts:
            output += part.write(self.materials)

            count += 1
            if count != len(self.parts):
                output += "\n"

        return output

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'ConfigPatch':
        yaml_materials : list[dict[str, Any]] | None = yaml.get('materials', None)
        if yaml_materials is None:
            raise ArgumentException("Materials list not defined")

        materials: dict[str, ConfigPartMaterialDef] = {}
        for yaml_material in yaml_materials:
            material = ConfigPartMaterialDef.from_yaml(yaml_material)
            materials[material.name] = material

        yaml_parts: list[dict[str, Any]] | None = yaml.get('parts', None)
        if yaml_parts is None:
            raise ArgumentException("Parts list not defined")

        parts = []
        for yaml_part in yaml_parts:
            part = ConfigPart.from_yaml(yaml_part)

            if part.restock_plus_name is not None:
                part_vanilla = copy.deepcopy(part)
                part_vanilla.name = part_vanilla.restock_plus_name

                part.restock_plus_name = None
                parts.append(part)
                parts.append(part_vanilla)

            else:
                parts.append(part)

        return ConfigPatch(
            materials=materials,
            parts=parts,
        )
