import sys
from pathlib import Path

from yaml import YAMLError
from yaml.parser import ParserError

from patch.configs import generate_material_configs
from patch.models import patch_models
from patch.patches import copy_patch_configs
from patch.assets import copy_prebuild_assets
from patch.textures import patch_textures
from patch.version import copy_version_file
from utils.exceptions import is_debugger_attached, CustomException
from utils.printing import header, error, warn


def patch_all(mod_name: str, patch_data_root_dir: Path, gamedata_dir: Path, texconv_path: Path | None):
    try:
        patch_data_asset_dir = patch_data_root_dir / "Assets"
        patch_data_patch_dir = patch_data_root_dir / "Patches"
        patch_data_material_dir = patch_data_root_dir / "Materials"
        patch_data_texture_dir = patch_data_root_dir / "Textures"
        patch_data_model_dir = patch_data_root_dir / "Models"

        output_mod_root_dir = Path(sys.argv[0]).parent.parent / "Output" / mod_name
        output_mod_asset_dir = output_mod_root_dir / "Assets"
        output_mod_material_dir = output_mod_root_dir / "Materials"
        output_mod_patch_dir = output_mod_root_dir / "Patches"

        compression_skipped = False

        header(f"Generating {mod_name}...")

        copy_version_file(
            patch_data_root_dir=patch_data_root_dir,
            output_mod_root_dir=output_mod_root_dir)

        copy_prebuild_assets(
            patch_data_asset_dir=patch_data_asset_dir,
            output_mod_asset_dir=output_mod_asset_dir)

        copy_patch_configs(
            patch_data_patch_dir=patch_data_patch_dir,
            output_mod_patch_dir=output_mod_patch_dir)

        generate_material_configs(
            patch_data_material_dir=patch_data_material_dir,
            output_mod_material_dir=output_mod_material_dir)

        patch_textures(
            patch_data_texture_dir=patch_data_texture_dir,
            output_mod_asset_dir=output_mod_asset_dir,
            gamedata_dir=gamedata_dir)

        if texconv_path is not None:
            # Lazy load the import
            from patch.compression import compress

            compress(
                output_mod_asset_dir=output_mod_asset_dir,
                texconv_path=texconv_path)
        else:
            warn("Skipping texture compression...")
            compression_skipped = True

        patch_models(
            patch_data_model_dir=patch_data_model_dir,
            output_mod_asset_dir=output_mod_asset_dir,
            gamedata_dir=gamedata_dir)

        if compression_skipped:
            warn("Texture compression was skipped, \n"
                 "Parts WILL NOT look right in game unless you manually convert them to DDS! \n"
                 "Installing the texconv-py package and setting the config \n"
                 "to point towards the texconv executable is HIGHLY recommended")

        header("Done!")
    except (BaseException, KeyboardInterrupt, YAMLError) as e:
        if isinstance(e, KeyboardInterrupt):
            warn("Process interrupted by user. Output may be incomplete. Exiting...")
            exit(1)

        if not is_debugger_attached():
            match e:
                case FileNotFoundError():
                    error(f"The file was not found: \r\n{e.filename}")
                case CustomException():
                    error(e.type_name + ": " + e.message, display_prefix=False)
                case ParserError():
                    if e.problem_mark is not None:
                        error(f"YAML Parse Error at line {e.problem_mark.line+1}, column {e.problem_mark.column+1} \n"
                              + str(e.problem))
                    else:
                        error("A YAML Parse Error occurred")
                case YAMLError():
                   if hasattr(e, 'problem_mark'):
                    error(f"YAML Parse Error at line {e.problem_mark.line+1}, column {e.problem_mark.column+1}")
                case _:
                    raise
        else:
            raise