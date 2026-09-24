import shutil
from pathlib import Path

from utils.printing import header, info
from utils.info_status import InfoStatus


def copy_prebuild_assets(patch_data_asset_dir: Path, output_mod_asset_dir: Path):
    header("Copying pre-built models and textures...")
    paths = [p for p in patch_data_asset_dir.glob('**/*.*') if p.suffix in ('.mu', '.dds')]
    for asset_file in paths:
        output_asset_relative_path = asset_file.relative_to(patch_data_asset_dir)

        output_asset_relative_path = output_asset_relative_path.parent.parent / output_asset_relative_path.name

        output_asset_file = Path(output_mod_asset_dir / output_asset_relative_path)
        output_asset_file.parent.mkdir(parents=True, exist_ok=True)

        printable_name = str(Path("Assets") / output_asset_relative_path)
        info(printable_name)

        shutil.copy(asset_file, output_asset_file)

        info(printable_name, status=InfoStatus.DONE)
