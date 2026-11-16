import sys
from pathlib import Path
from time import sleep

from yaml import YAMLError
from yaml.parser import ParserError

from patch.models import patch_models
from patch.configs import copy_patch_configs
from patch.assets import copy_prebuild_assets
from patch.textures import patch_textures
from patch.version import copy_version_file
from utils.exceptions import is_debugger_attached, CustomException
from utils.printing import header, error, warn


def patch_all(patch_data_root_dir: Path,
              gamedata_dir: Path,
              texconv_path: Path | None,
              single_texture: Path | None,
              single_model: Path | None):
    try:
        mod_name = patch_data_root_dir.name

        patch_data_asset_dir = patch_data_root_dir / "Assets"
        patch_data_patch_dir = patch_data_root_dir / "Configs"
        patch_data_texture_dir = patch_data_root_dir / "Textures"
        patch_data_model_dir = patch_data_root_dir / "Models"

        output_root_dir = Path(sys.argv[0]).parent.parent / "Output"
        output_mod_root_dir = output_root_dir / mod_name
        output_mod_asset_dir = output_mod_root_dir / "Assets"
        output_mod_patch_dir = output_mod_root_dir / "Patches"

        single_texture_path = patch_data_texture_dir / single_texture if single_texture is not None else None
        single_model_path = patch_data_model_dir / single_model if single_model is not None else None

        compression_skipped = False

        header(f"Generating {mod_name}...")
        sleep(0.5)

        copy_version_file(
            patch_data_root_dir=patch_data_root_dir,
            output_mod_root_dir=output_mod_root_dir)

        if (single_model_path is None and single_texture_path is None) or (single_model_path is not None):
            patch_models(
                patch_data_model_dir=patch_data_model_dir,
                output_mod_asset_dir=output_mod_asset_dir,
                output_root_dir=output_root_dir,
                gamedata_dir=gamedata_dir,
                single_model_path=single_model_path)

        copy_prebuild_assets(
            patch_data_asset_dir=patch_data_asset_dir,
            output_mod_asset_dir=output_mod_asset_dir)

        copy_patch_configs(
            patch_data_patch_dir=patch_data_patch_dir,
            output_mod_patch_dir=output_mod_patch_dir)

        if (single_model_path is None and single_texture_path is None) or (single_texture_path is not None):
            if texconv_path is None:
                warn("Skipping texture compression...")
                compression_skipped = True

            patch_textures(
                patch_data_texture_dir=patch_data_texture_dir,
                output_mod_asset_dir=output_mod_asset_dir,
                gamedata_dir=gamedata_dir,
                texconv_path=texconv_path,
                single_texture_path=single_texture_path)

            if compression_skipped:
                warn("Texture compression was skipped, \n"
                     "Parts WILL NOT look right in game unless you manually convert them to DDS! \n"
                     "Installing the texconv-py package and setting the config \n"
                     "to point towards the location of a texconv executable is HIGHLY recommended")

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