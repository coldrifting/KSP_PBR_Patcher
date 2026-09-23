import shutil
from pathlib import Path

from utils.terminal_colors import header, info, InfoStatus


def copy_prebuild_assets(input_asset_dir: Path, output_asset_dir: Path):
    header("Copying pre-built models and textures...")
    paths = [p for p in input_asset_dir.glob('**/*.*') if p.suffix in ('.mu', '.dds')]
    for asset_file in paths:
        output_asset_relative_path = asset_file.relative_to(input_asset_dir)

        output_asset_relative_path = output_asset_relative_path.parent.parent / output_asset_relative_path.name

        output_asset_file = Path(output_asset_dir / output_asset_relative_path)
        output_asset_file.parent.mkdir(parents=True, exist_ok=True)

        printable_name = str(Path("Assets") / output_asset_relative_path)
        info(printable_name)

        shutil.copy(asset_file, output_asset_file)

        info(printable_name, status=InfoStatus.DONE)
