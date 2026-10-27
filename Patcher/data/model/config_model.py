import errno
import os
import shutil
from pathlib import Path
from typing import Any

from data.model.operations.edit_material_textures import OperationEditMaterialTextures
from data.model.operations.operation_factory import OperationFactory
from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from data.model.color_zone import ColorZones
from utils.exceptions import ArgumentException
from utils.printing import warn
from utils.config_writer import ConfigWriter


class ConfigModel:
    def __init__(self,
                 part: str,
                 model: str,
                 after: str | None,
                 needs: list[str],
                 override: bool | None,
                 remove_part_variants: bool,
                 dlc: str | None,
                 color_zones: ColorZones | None,
                 operations: list[Operation]):
        self.part = part
        self.model = Path(model)
        self.after = after
        self.needs = needs
        self.override = override
        self.remove_part_variants = remove_part_variants
        self.dlc = dlc
        self.color_zones = color_zones
        self.operations = operations

    def __str__(self):
        return "ConfigModel: " + self.model.name

    def apply(self, game_data_dir: Path, output_root_dir: Path, asset_output_dir: Path):
        if len(self.operations) < 1 and self.color_zones is None:
            warn(f"{self.model} has no operations or color zones defined")
            return

        source_file = Path(game_data_dir / self.model)
        if not source_file.exists():
            source_file = Path(game_data_dir / Path(self.model).with_suffix(".mu"))
            if not source_file.exists():
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), source_file)

        mu_data = MuData.from_file(source_file)
        for operation in self.operations:
            operation.apply(mu_data)

        if self.color_zones is not None:
            self.color_zones.apply_model_changes(mu_data)

        #mu_data.remove_unused_materials()

        output_file = asset_output_dir / Path(self.model).with_suffix(".mu").name
        output_file.parent.mkdir(parents=True, exist_ok=True)
        mu_data.write_file(output_file)

        # Copy textures
        for texture in mu_data.textures:
            texture_source = (source_file.parent / texture.name).with_suffix(".dds")
            if not texture_source.exists():
                continue

            texture_dest = (output_file.parent / texture.name).with_suffix(".dds")
            shutil.copyfile(texture_source, texture_dest)

        # Copy textures from different folders as defined in config
        for operation in self.operations:
            if isinstance(operation, OperationEditMaterialTextures):
                ConfigModel.copy_texture_with_path(game_data_dir, output_file.parent, operation.main_tex)
                ConfigModel.copy_texture_with_path(game_data_dir, output_file.parent, operation.bump_map)
                ConfigModel.copy_texture_with_path(game_data_dir, output_file.parent, operation.emissive)
                ConfigModel.copy_texture_with_path(game_data_dir, output_file.parent, operation.metal_map)
                ConfigModel.copy_texture_with_path(game_data_dir, output_file.parent, operation.team_color_map)

        # Generate patch file to replace models
        config_file = output_file.with_suffix(".cfg")

        config_text = self.write_config(
            output_root_dir=output_root_dir,
            output_file=output_file)

        config_file.write_text(config_text)

    def write_config(self, output_root_dir: Path, output_file: Path) -> str:
        writer: ConfigWriter = ConfigWriter()

        selector = f"@PART[{self.part}]"

        mod_name = self.model.parts[0]
        if mod_name.lower() == "restock":
            selector += ":HAS[~RestockIgnore[*]]"

        if len(self.needs) > 0:
            selector += ":NEEDS[" + ",".join(self.needs) + "]"

        if self.after is not None:
            selector += f":AFTER[{self.after}]"

        # Start part
        writer.indent(selector)

        if self.remove_part_variants:
            writer.write()
            writer.write("!MODULE[ModulePartVariants],* {}")

        model_find = str(self.model).replace('\\', '/')
        model_replace = str(output_file.with_suffix('').relative_to(output_root_dir)).replace('\\', '/')

        if self.override:
            writer.write("!mesh = DELETE")
            writer.write("!MODEL,* {}")
            writer.indent("MODEL")
            writer.write(f" model = {model_replace}")
            writer.unindent()
        else:
            writer.indent(f"@MODEL,*:HAS[#model[{model_find}]]")
            writer.write(f"%model = {model_replace}")
            writer.unindent()

        # Generate color zones from config
        if self.color_zones is not None:
            self.color_zones.write_config(writer)

        writer.unindent()

        return writer.string

    @staticmethod
    def copy_texture_with_path(game_data_dir: Path, output_folder: Path, texture_path: Path | None):
        if texture_path is not None:
            if len(texture_path.parents) > 0 and texture_path.parent != Path('.'):
                source_tex = game_data_dir / texture_path.with_suffix(".dds")
                if not source_tex.exists():
                    raise ArgumentException(f"Unable to find texture at location: {source_tex}")

                dest_text = output_folder / texture_path.with_suffix(".dds").name
                shutil.copyfile(source_tex, dest_text)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'ConfigModel':
        part = yaml.get("part", None)
        if part is None or not isinstance(part, str):
            raise ArgumentException("Missing required parameter part")

        model = yaml.get("model", None)
        if model is None or not isinstance(model, str):
            raise ArgumentException("Missing required parameter model")

        after = yaml.get("after", None)
        needs = yaml.get("needs", [])

        override: bool | None = yaml.get("override", None)
        remove_part_variants: bool = yaml.get("remove_part_variants", False)

        color_zones: ColorZones | None = None
        color_zones_yaml: dict[str, Any] | None = yaml.get("color_zones", None)
        if color_zones_yaml is not None:
            color_zones = ColorZones.from_yaml(part, color_zones_yaml)

        operations: list[Operation] = []
        operations_yaml: list[dict[str, Any]] | None = yaml.get("operations", None)
        if operations_yaml is None:
            operations = []
        else:
            for operation_yaml in operations_yaml:
                operation = OperationFactory.from_yaml(operation_yaml)
                operations.append(operation)


        return ConfigModel(
            part=part,
            model=model,
            after=after,
            needs=needs,
            override=override,
            remove_part_variants=remove_part_variants,
            dlc=yaml.get("dlc", None),
            color_zones=color_zones,
            operations=operations
        )
