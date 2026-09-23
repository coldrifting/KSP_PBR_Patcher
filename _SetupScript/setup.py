import argparse
import errno
import os
import shutil
import sys
from pathlib import Path

from yaml import YAMLError
from yaml.parser import ParserError

from setup.compress import compress
from setup.generate_configs import generate_material_configs
from setup.models import patch_models
from setup.patches import copy_patch_configs
from setup.prebuilt_assets import copy_prebuild_assets
from setup.textures import patch_textures
from setup.version import copy_version_file
from utils.exceptions import is_debugger_attached, CustomException
from utils.terminal_colors import header, error, warn
from utils.texconv_locator import locate_texconv
from utils.verify_packages import verify_packages

verify_packages()

parser = argparse.ArgumentParser(description="Creates a KSP mod that adds PBR support for a given mod "
                                             "by copying and patching assets from the target mod")

parser.add_argument("--mod-folder",
                    type=str,
                    required=True,
                    help="The location of the patcher assets for a mod")

parser.add_argument("--gamedata-folder",
                    type=str,
                    required=True,
                    help="The location of your KSP gamedata directory containing the mod you wish to patch")


parser.add_argument("--texconv-path",
                    type=str,
                    required=False,
                    help="The location of the texconv executable for converting images into compressed dds files")

args = parser.parse_args()

try:
    texconv_path = locate_texconv(args.texconv_path)

    gamedata_dir = Path(args.gamedata_folder)
    if not gamedata_dir.exists():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), gamedata_dir)

    if args.texconv_path is None:
        warn("Missing optional parameter --texconv-path")
        warn("Attempting to locate texconv in the system PATH")

    input_root_dir = Path(args.mod_folder)
    input_resource_dir = Path(input_root_dir / "Resources")
    input_asset_dir = Path(input_resource_dir / "Assets")
    input_material_dir = Path(input_resource_dir / "Materials")
    input_patch_dir = Path(input_resource_dir / "Patches")

    mod_name = None
    for version_file in input_resource_dir.glob("*.version"):
        with open(version_file, "r") as version_file_text:
            version_file_text.readline()
            info = version_file_text.readline()
            infos = [x.strip().rstrip(",").rstrip("\"").lstrip("\"".strip()) for x in info.split(":")]
            if len(info) >= 2:
                mod_name = infos[1]

    if mod_name is None:
        error("Unable to find mod version file in resources directory")

    output_root_dir = Path(input_root_dir / "GameData" / mod_name)
    output_asset_dir = Path(output_root_dir / "Assets")
    output_material_dir = Path(output_root_dir / "Materials")
    output_patch_dir = Path(output_root_dir / "Patches")

    header(f"Generating {mod_name}...")

    copy_patch_configs(
        input_patch_dir=input_patch_dir,
        output_patch_dir=output_patch_dir)

    generate_material_configs(
        input_material_dir=input_material_dir,
        output_material_dir=output_material_dir)

    copy_prebuild_assets(
        input_asset_dir=input_asset_dir,
        output_asset_dir=output_asset_dir)

    patch_textures(
        input_asset_dir=input_asset_dir,
        output_asset_dir=output_asset_dir,
        gamedata_dir=gamedata_dir
    )

    copy_version_file(
        input_resource_dir=input_resource_dir,
        output_root_dir=output_root_dir
    )

    if texconv_path is not None:
        compress(
            output_asset_dir=output_asset_dir,
            texconv_path=texconv_path
        )
    else:
        warn("Skipping texture compression...")

    patch_models(
        input_asset_dir=input_asset_dir,
        output_asset_dir=output_asset_dir,
        gamedata_dir=gamedata_dir
    )

    header("Done!")
except (BaseException, KeyboardInterrupt, YAMLError) as e:
    if isinstance(e, KeyboardInterrupt):
        warn("Process interrupted by user. Output may be incomplete. Exiting...")
        exit(1)

    if not False: #is_debugger_attached():
        match e:
            case FileNotFoundError():
                error(f"The file was not found: \r\n{e.filename}")
            case CustomException():
                error(e.type_name + ": " + e.message, display_prefix=False)
            case ParserError():
                error(f"YAML Parse Error at line {e.problem_mark.line+1}, column {e.problem_mark.column+1} \n"
                      + str(e.problem))
            case YAMLError():
               if hasattr(e, 'problem_mark'):
                error(f"YAML Parse Error at line {e.problem_mark.line+1}, column {e.problem_mark.column+1}")
            case _:
                raise
    else:
        raise