import argparse
import errno
import importlib
import os
import sys
from pathlib import Path

from utils.printing import error, warn, header
from utils.terminal_colors import TerminalColors
from utils.texconv_locator import locate_texconv


def ensure_package(package_name, import_name=None):
    if import_name is None:
        import_name = package_name

    try:
        importlib.import_module(import_name)
    except ImportError:
        requirements_file = Path(Path(sys.argv[0]).parent / Path("requirements.txt")).resolve()
        error(f"Required package {package_name} not found \r\n"
              f"You can run the following command in a command prompt with administrator "
              f"rights to install all required and recommended packages for this script: \r\n"
              f"python -m pip install -r \"{requirements_file}\"")

def check_package(package_name, import_name=None):
    if import_name is None:
        import_name = package_name

    try:
        importlib.import_module(import_name)
    except ImportError:
        requirements_file = Path(Path(sys.argv[0]).parent / Path("requirements.txt")).resolve()
        warn(f"Recommended package {package_name} not found \r\n"
              f"Some functionality may be disabled \r\n"
              f"You can run the following command in a command prompt with administrator "
              f"rights to install all required and recommended packages for this script: \r\n"
              f"python -m pip install -r \"{requirements_file}\"")

ensure_package("pyaml", "yaml")
ensure_package("pillow", "PIL")
ensure_package("numpy")
ensure_package("cairosvg")
ensure_package("scipy")
check_package("texconv-py", "texconv")

parser = argparse.ArgumentParser(description="Creates a KSP mod that adds PBR support for a given mod "
                                             "by copying and patching assets from the target mod")

parser.add_argument("--mod-name",
                    type=str,
                    required=False,
                    help="The name of a mod to patch, with it's assets located in the Mods folder")

parser.add_argument("--gamedata-folder",
                    type=str,
                    required=False,
                    help="The location of your KSP gamedata directory containing the mod you wish to patch")

parser.add_argument("--texconv-path",
                    type=str,
                    required=False,
                    help="The location of the texconv executable for converting images into compressed dds files")

args = parser.parse_args()

if 'texconv' in sys.modules:
    texconv_path = locate_texconv(args.texconv_path)
else:
    texconv_path = None

if args.gamedata_folder is None:
    ksp_root = os.getenv("KSPRoot")
    if ksp_root is None:
        error("No --gamedata-folder parameter passed to script, and the KSPRoot environemntal variable was not defined")
        exit(1)

    gamedata_dir = Path(ksp_root) / "GameData"
else:
    gamedata_dir = Path(args.gamedata_folder)

if not gamedata_dir.exists():
    error(f"Unable to find gamedata folder at provided path: {gamedata_dir}. Does it exist?")
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), gamedata_dir)

# Loaded last to give us time to check for imports
from patch.all import patch_all

if args.mod_name is not None:
    patch_data_root_dir = Path(sys.argv[0]).parent.parent / "Data" / args.mod_name
    if not patch_data_root_dir.exists():
        error(f"Unable to find {args.mod_name} patch files in the Data folder.\n"
              f"Does {patch_data_root_dir} exist?")

    patch_all(patch_data_root_dir=patch_data_root_dir,
              gamedata_dir=gamedata_dir,
              texconv_path=texconv_path)

else:
    mods: list[str] = []
    patch_mods_dir = Path(sys.argv[0]).parent.parent / "Data"
    for mod_dir in patch_mods_dir.iterdir():
        mods.append(mod_dir.name)

    input_indices: list[int] = []

    while not input_indices:
        header("The following PBR patch mod generators were found: ")
        for index, mod in enumerate(mods):
            print(TerminalColors.CYAN + str(index + 1) + TerminalColors.ENDC + ": " + mod)
        print("Input a range of numbers to select which patches you would like to generate (e.g. 1, 3-5): \n"
             "Press enter to generate all patches")

        try:
            input_indices = []

            input_value = input()
            if input_value.strip() == '':
                input_indices = [x for x in range(len(mods))]

            else:
                segments = [x.strip() for x in input_value.split(",")]
                for segment in segments:
                    splits = [y.strip() for y in segment.split("-")]
                    if len(splits) > 2:
                        raise ValueError("Invalid format")
                    if len(splits) == 1:
                        num = int(splits[0])
                        if num in input_indices:
                            raise ValueError("Already selected")

                        if num < 1 or num > len(mods):
                            raise ValueError(f"Invalid selection. Patcher with index {num} does not exist")

                        input_indices.append(num)
                    if len(splits) == 2:
                        start = int(splits[0])
                        end = int(splits[1])

                        for i in range(start, end + 1):
                            if i in input_indices:
                                raise ValueError("Already selected")

                            if i < 1 or i > len(mods):
                                raise ValueError(f"Invalid selection. Patcher with index {i} does not exist")
                            input_indices.append(i)

        except ValueError as e:
            print(TerminalColors.YELLOW + str(e) + TerminalColors.ENDC)
            input_indices = []

    for mod_index in input_indices:
        patch_data_root_dir = Path(sys.argv[0]).parent.parent / "Data" / mods[mod_index - 1]
        patch_all(patch_data_root_dir=patch_data_root_dir,
                  gamedata_dir=gamedata_dir,
                  texconv_path=texconv_path)