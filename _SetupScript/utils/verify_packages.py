import importlib
import sys
from pathlib import Path


def ensure_package(package_name, import_name=None):
    if import_name is None:
        import_name = package_name

    try:
        importlib.import_module(import_name)
    except ImportError:
        requirements_file = Path(Path(sys.argv[0]).parent / Path("requirements.txt")).resolve()
        raise ModuleNotFoundError(f"Required package {package_name} not found\r\n"
              f"You can run the following command in a command prompt with administrator "
              f"rights to install all required packages for this script:\r\n"
              f"python -m pip install -r \"{requirements_file}\"")

def verify_packages():
    ensure_package("pyaml", "yaml")
    ensure_package("pillow", "PIL")
    ensure_package("numpy")
    ensure_package("cairosvg")
    ensure_package("texconv-py", "texconv")