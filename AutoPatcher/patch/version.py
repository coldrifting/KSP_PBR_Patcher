import shutil
from pathlib import Path

from utils.printing import header, info
from utils.info_status import InfoStatus


def copy_version_file(patch_data_root_dir: Path, output_mod_root_dir: Path):
    header("Copying version file...")
    for version_file in patch_data_root_dir.glob("**/*.version"):
        output_version_file = Path(output_mod_root_dir / version_file.name)
        output_version_file.parent.mkdir(parents=True, exist_ok=True)

        info(version_file.name)

        shutil.copy(version_file, output_version_file)

        info(version_file.name, status=InfoStatus.DONE)
