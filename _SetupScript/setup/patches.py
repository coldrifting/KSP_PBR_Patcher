import shutil
from pathlib import Path

from utils.terminal_colors import header, info, InfoStatus


def copy_patch_configs(input_patch_dir: Path, output_patch_dir: Path):
    header("Copying patch configs...")
    for patch_file in input_patch_dir.glob("**/*.cfg"):
        output_patch_relative_path = patch_file.relative_to(input_patch_dir)
        output_patch_file = Path(output_patch_dir / output_patch_relative_path)
        output_patch_file.parent.mkdir(parents=True, exist_ok=True)

        printable_name = str(Path("Patches") / output_patch_relative_path)
        info(printable_name)

        shutil.copy(patch_file, output_patch_file)

        info(printable_name, status=InfoStatus.DONE)
