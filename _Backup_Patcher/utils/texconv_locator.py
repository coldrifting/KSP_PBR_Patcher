import shutil
from pathlib import Path

from utils.printing import warn


def locate_texconv(texconv_path: str | None) -> Path | None:
    if texconv_path is None:
        return auto_locate_texconv()

    if not Path(texconv_path).exists():
        warn(f"The texconv executable was not found at the location below: \n"
             f"{texconv_path} \n"
             f"If this location is incorrect, please update the Texconv_Path variable in the Setup.bat file \n"
             f"Attempting to locate texconv in the system PATH...")

        return auto_locate_texconv()
    else:
        return Path(texconv_path)


def auto_locate_texconv() -> Path | None:
    auto_texconv_path: str | None = shutil.which("texconv")
    if auto_texconv_path is None:
        warn("Unable to locate texconv executable in system PATH.\n "
             "DDS Compression has been disabled, textures will not display correctly! \n"
             "Please find a texconv executable compatible with your system."
             "Alternatively, you can manually compress all png files in the output folder to dds")
        return None
    else:
        return Path(auto_texconv_path)
