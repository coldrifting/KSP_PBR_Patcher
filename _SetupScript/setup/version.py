import shutil
from pathlib import Path

from utils.terminal_colors import header, info, InfoStatus


def copy_version_file(input_resource_dir: Path, output_root_dir: Path):
    header("Copying version file...")
    for version_file in input_resource_dir.glob("**/*.version"):
        output_version_file = Path(output_root_dir / version_file.name)
        output_version_file.parent.mkdir(parents=True, exist_ok=True)

        info(version_file.name)

        shutil.copy(version_file, output_version_file)

        info(version_file.name, status=InfoStatus.DONE)
