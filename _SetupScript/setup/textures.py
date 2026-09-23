from pathlib import Path

from setup.model_or_texture import patch_model_or_textures
from utils.terminal_colors import header


def patch_textures(input_asset_dir: Path, output_asset_dir: Path, gamedata_dir: Path):
    header("Processing textures...")
    patch_model_or_textures(
        input_asset_dir=input_asset_dir,
        output_asset_dir=output_asset_dir,
        gamedata_dir=gamedata_dir,
        is_model=False)
