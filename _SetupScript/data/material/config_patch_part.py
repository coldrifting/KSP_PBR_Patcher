from typing import Any, Tuple

from data.material.material_apply import ConfigPartMaterialApplication
from data.material.material_def import ConfigPartMaterialDef
from utils.exceptions import ArgumentException
from utils.string_writer import StringWriter


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
        self.models_find_and_replace = models_find_and_replace
        self.restock_plus_name = restock_plus_name

    def write(self, material_definitions: dict[str, ConfigPartMaterialDef]) -> str:

        # ZoneName: (tc1, tc2, transforms)
        zones: dict[str, Tuple[str, str, list[str]]] = {}
        for material in self.materials:
            if material.name not in material_definitions.keys():
                raise ArgumentException(message=f"Material name {material.name} not found in material definitions")

            base = (material_definitions[material.name].tc1, material_definitions[material.name].tc2, [])
            zn = zones.get(material.zone, base)
            if material.target_transforms is not None:
                zn[2].extend(material.target_transforms)

            zones[material.zone] = zn

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

        if self.models_find_and_replace is not None:
            for model in self.models_find_and_replace:
                writer.indent(f"@MODEL,*:HAS[#model[{model.find}]]")
                writer.write(f"%model = {model.replace}")
                writer.unindent()

        # Start ModuleTechnicolor
        writer.indent("MODULE")

        writer.write("name = ModuleTechnicolor")
        writer.write()

        for zone_name, material_info in zones.items():
            if material_info[0] is not None:
                writer.indent("COLORZONE")

                writer.write(f"name = {zone_name}")
                writer.write(f"swatchPrimary = {material_info[0][0]}")
                writer.write(f"swatchSecondary = {material_info[1][0]}")

                if len(material_info[2]) > 0:
                    for transform_name in material_info[2]:
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

        models: list[ConfigPartModelFindAndReplace] | None = []
        models_find_and_replace_yaml: list[dict[str, Any]] | None = yaml.get("models", None)
        if models_find_and_replace_yaml is None:
            models = None
        else:
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
