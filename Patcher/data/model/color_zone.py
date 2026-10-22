from copy import deepcopy
from typing import Any

from data.model.mu_data import MuData
from data.model.types.tag.tag_mu import MuTag
from data.model.types.transform import Transform
from utils.config_writer import ConfigWriter
from utils.exceptions import ArgumentException
from utils.team_color import TeamColor
from utils.yaml_load import get_yaml_parameter


class ColorZone:
    def __init__(self,
                 name: str,
                 tc1: str,
                 tc2: str | None,
                 copy: str | None,
                 materials_filter: list[str],
                 transforms_filter: list[str]):
        self.name = name
        self.tc1 = tc1
        self.tc2 = tc2
        self.copy = copy
        self.materials_filter = materials_filter
        self.transforms_filter = transforms_filter
        self.transforms: list[Transform] = []

    @staticmethod
    def from_yaml(name, yaml: dict[str, Any]) -> 'ColorZone':
        name: str = name
        tc1: str = get_yaml_parameter(yaml, "tc1", str)
        tc2: str | None = yaml.get("tc2", None)
        copy: str | None = yaml.get("copy", None)
        materials_filter: list[str] = yaml.get("materials", [])
        transforms_filter: list[str] = yaml.get("transforms", [])

        return ColorZone(
            name=name,
            tc1=tc1,
            tc2=tc2,
            copy=copy,
            materials_filter=materials_filter,
            transforms_filter=transforms_filter)


class ColorZones:
    def __init__(self, name: str, zones: dict[str, ColorZone]):
        self.name = name # Part Name
        self.zones = zones

    def apply_model_changes(self, mu_data: MuData):
        renderable_tags = {MuTag.MeshRenderer, MuTag.SkinnedMeshRenderer}
        all_renderable_transforms = mu_data.get_transforms(None, renderable_tags)

        # Filter by transform and/or materials
        for zone in self.zones.values():
            if len(zone.transforms_filter) == 0:
                zone.transforms.extend(all_renderable_transforms)
            else:
                for transform in all_renderable_transforms:
                    if transform.name in zone.transforms_filter:
                        zone.transforms.append(transform)

            if len(zone.materials_filter) > 0:
                valid_material_indices: list[int] = []
                for i in range(len(mu_data.materials)):
                    material = mu_data.materials[i]
                    if material.name in zone.materials_filter:
                        valid_material_indices.append(i)

                for i in reversed(range(len(zone.transforms))):
                    transform = zone.transforms[i]
                    if MuTag.MeshRenderer in transform:
                        renderer = zone.transforms[i][MuTag.MeshRenderer]
                        if renderer.material_index not in valid_material_indices:
                            del zone.transforms[i]
                    elif MuTag.SkinnedMeshRenderer in transform:
                        skinned_mesh = zone.transforms[i][MuTag.SkinnedMeshRenderer]
                        for index in skinned_mesh.material_indices:
                            if index not in valid_material_indices:
                                del zone.transforms[i]
                    else:
                        raise NotImplementedError()

                if len(zone.transforms) == 0:
                   error_msg = "No transforms found matching the following filters: \n"
                   if len(zone.transforms) > 0:
                       error_msg += "Transforms: \n"
                       for transform in zone.transforms:
                           error_msg += f"{transform} \n"

                   if len(zone.materials_filter) > 0:
                       error_msg += "Materials: \n"
                       for material in zone.materials_filter:
                           error_msg += f"{material} \n"

                   raise ArgumentException(error_msg)

        # Make zones exclusive to a single transform
        used_transforms: list[Transform] = []
        for zone in reversed(self.zones.values()):
            for i in reversed(range(len(zone.transforms))):
                if zone.transforms[i] in used_transforms:
                    del zone.transforms[i]
                else:
                    used_transforms.append(zone.transforms[i])

        # Apply material changes to model
        for zone_name, zone in self.zones.items():
            tc1, tc2 = TeamColor.get_colors(zone.tc1, zone.tc2)
            if zone.copy is not None:
                new_material = deepcopy(mu_data.materials[zone.copy])
                new_material.name = zone.copy + "-" + zone_name
                mu_data.materials.append(new_material)
                mu_data.assign_team_colors(new_material.name, tc1, tc2)

                new_material_index = len(mu_data.materials) - 1
                for transform in zone.transforms:
                    transform.assign_material_index(new_material_index)
            else:
                materials_indices_to_fix: set[int] = set()
                for transform in zone.transforms:
                    mat_index = transform.get_material_index()
                    materials_indices_to_fix.add(mat_index)

                for material_index in materials_indices_to_fix:
                    material = mu_data.materials[material_index]
                    mu_data.assign_team_colors(material.name, tc1, tc2)

    def write_config(self, writer: ConfigWriter):
        writer.write()
        writer.write("!MODULE[ModuleTechnicolor],* {}")
        writer.indent("MODULE")
        writer.write("name = ModuleTechnicolor")
        writer.write()

        for zone_name, zone in self.zones.items():
            writer.indent("COLORZONE")

            writer.write(f"name = {zone_name}")
            writer.write(f"swatchPrimary = {zone.tc1}")
            writer.write(f"swatchSecondary = {zone.tc2 if zone.tc2 is not None else 'blank'}")
            for transform in zone.transforms:
                writer.write(f"transform = {transform}")

            writer.unindent()

        writer.unindent()

    @staticmethod
    def from_yaml(part_name: str, yaml: dict[str, Any]) -> 'ColorZones':
        zones: dict[str, ColorZone] = {}

        for zone_name, zone in yaml.items():
            zones[zone_name] = ColorZone.from_yaml(zone_name, zone)

        if len(zones) < 1:
            raise ValueError("No zones found")

        return ColorZones(part_name, zones)
