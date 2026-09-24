import argparse
import errno
import importlib
import os
import sys
from pathlib import Path

from utils.printing import error, warn
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
                    required=True,
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

patch_data_root_dir = Path(sys.argv[0]).parent.parent / "Data" / args.mod_name
if not patch_data_root_dir.exists():
    error(f"Unable to find {args.mod_name} patch files in the Data folder.\n"
          f"Does {patch_data_root_dir} exist?")

# Loaded last to give us time to check for imports
from patch.all import patch_all

patch_all(mod_name=args.mod_name,
          patch_data_root_dir=patch_data_root_dir,
          gamedata_dir=gamedata_dir,
          texconv_path=texconv_path)
