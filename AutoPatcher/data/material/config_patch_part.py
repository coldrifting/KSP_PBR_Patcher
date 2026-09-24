from typing import Any

from data.material.material_apply import ConfigPartMaterialApplication
from data.material.material_def import ConfigPartMaterialDef
from utils.exceptions import ArgumentException
from utils.string_writer import StringWriter
from utils.team_color import TeamColor


class ConfigPartModelFindAndReplace:
    def __init__(self, find: str, replace: str):
        self.find = find
        self.replace = replace

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'ConfigPartModelFindAndReplace':
        find: str | None = yaml.get("find", None)
        if find is None:
            raise ArgumentException("Missing find value for part model find and replace")

        replace: str | None = yaml.get("replace", None)
        if replace is None:
            raise ArgumentException("Missing replace value for part model find and replace")

        return ConfigPartModelFindAndReplace(find, replace)


class ZoneInfo:
    def __init__(self, tc1: TeamColor, tc2: TeamColor | None, transforms: list[str]):
        self.tc1 = tc1
        self.tc2 = tc2
        self.transforms = transforms

    def extend_transforms(self, transforms: list[str]):
        self.transforms.extend(transforms)

class ConfigPart:
    def __init__(self,
                 name: str,
                 materials: list[ConfigPartMaterialApplication],
                 after: str | None = None,
                 remove_part_variants: bool = False,
                 models_find_and_replace: list[ConfigPartModelFindAndReplace] | None = None,
                 restock_plus_name: str | None = None):
        self.name = name
        self.materials = materials
        self.after = after
        self.remove_part_variants = remove_part_variants
        self.models_find_and_replace: list[ConfigPartModelFindAndReplace] = [] if models_find_and_replace is None else models_find_and_replace
        self.restock_plus_name = restock_plus_name

    def write(self, material_definitions: dict[str, ConfigPartMaterialDef]) -> str:

        # ZoneName: (tc1, tc2, transforms)
        zones: dict[str, ZoneInfo] = {}
        for material in self.materials:
            mat = material_definitions.get(material.name, None)
            if mat is None:
                raise ArgumentException(message=f"Material name {material.name} not found in material definitions")

            if mat.tc1 is None:
                continue

            zone_info = zones.get(material.zone, ZoneInfo(tc1=mat.tc1, tc2=mat.tc2, transforms=[]))
            if material.target_transforms is not None:
                zone_info.extend_transforms(material.target_transforms)

            zones[material.zone] = zone_info

        writer: StringWriter = StringWriter()

        selector = "@PART["
        selector += self.name
        selector += "]"
        if self.after is not None:
            if self.after.lower() == "restock":
                selector += ":HAS[~RestockIgnore[*]]"

            selector += ":AFTER["
            if self.restock_plus_name is not None:
                selector += "ReStockPlus"
                selector += "]:NEEDS[!SquadExpansion/MakingHistory"
            else:
                selector += self.after
            selector += "]"

        # Start part
        writer.indent(selector)

        if self.remove_part_variants:
            writer.write("!MODULE[ModulePartVariants],* {}")

        if len(self.models_find_and_replace) > 0:
            for model in self.models_find_and_replace:
                writer.indent(f"@MODEL,*:HAS[#model[{model.find}]]")
                writer.write(f"%model = {model.replace}")
                writer.unindent()

        # Start ModuleTechnicolor
        writer.indent("MODULE")

        writer.write("name = ModuleTechnicolor")
        writer.write()

        for zone_name, zone_info in zones.items():
            writer.indent("COLORZONE")

            writer.write(f"name = {zone_name}")
            writer.write(f"swatchPrimary = {zone_info.tc1.name}")
            writer.write(f"swatchSecondary = {zone_info.tc2.name if zone_info.tc2 is not None else 'blank'}")

            if len(zone_info.transforms) > 0:
                for transform_name in zone_info.transforms:
                    writer.write(f"transform = {transform_name}")

            # End COLORZONE
            writer.unindent()

        # End ModuleTechnicolor
        writer.unindent()

        for material in self.materials:
            writer.indent("SHABBY_MATERIAL_REPLACE")

            writer.write(f"materialDef = {material.name}")

            if material.target_transforms is None:
                writer.write(f"targetMaterial = {material.target_material}")
            else:
                for transform_name in material.target_transforms:
                    writer.write(f"targetTransform = {transform_name}")

                if material.ignore_transforms is not None:
                    for transform_name in material.ignore_transforms:
                        writer.write(f"ignoreMesh = {transform_name}")

            # End SHABBY_MATERIAL_REPLACE
            writer.unindent()

        # End part
        writer.unindent()

        return writer.get_string()

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'ConfigPart':
        name: str | None = yaml.get("name", None)
        if name is None:
            raise ArgumentException("Missing name value for part")

        materials_yaml: list[dict[str, Any]] | None = yaml.get("materials", None)
        if materials_yaml is None:
            raise ArgumentException("Missing materials list for part")

        materials: list[ConfigPartMaterialApplication] = []
        for material in materials_yaml:
            material = ConfigPartMaterialApplication.from_yaml(material)
            materials.append(material)

        after: str | None = yaml.get("after", None)

        restock_plus_name: str | None = yaml.get("restock_plus_name", None)

        remove_part_variants = yaml.get("remove_part_variants", False)

        models: list[ConfigPartModelFindAndReplace] = []
        models_find_and_replace_yaml: list[dict[str, Any]] | None = yaml.get("models", None)
        if models_find_and_replace_yaml is not None:
            for model_yaml in models_find_and_replace_yaml:
                model = ConfigPartModelFindAndReplace.from_yaml(model_yaml)
                models.append(model)

        return ConfigPart(
            name=name,
            materials=materials,
            after=after,
            remove_part_variants=remove_part_variants,
            models_find_and_replace=models,
            restock_plus_name=restock_plus_name
        )
