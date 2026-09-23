from pathlib import Path

import yaml

from data.model.config_model import ConfigModel
from data.texture.config_texture import ConfigTexture
from utils.terminal_colors import info, InfoStatus


def patch_model_or_textures(input_asset_dir: Path, output_asset_dir: Path, gamedata_dir: Path, is_model: bool):
    for asset in input_asset_dir.glob("**/*.yaml"):
        asset_name = asset.name.rstrip(".yaml")
        asset_sub_path = str(asset.parent.parent.relative_to(input_asset_dir)).rstrip(".yaml")
        asset_output_subdir = output_asset_dir / asset_sub_path
        asset_relative_path = str(Path(asset_sub_path) / Path(asset_name))

        info_written = False
        try:
            with open(asset) as f:
                yaml_dict = yaml.safe_load(f)

                if is_model:
                    yaml_models = yaml_dict.get('model', None)
                    if yaml_models is None:
                        continue
                else:
                    yaml_textures = yaml_dict.get('texture', None)
                    if yaml_textures is None:
                        continue

            info(asset_relative_path)
            info_written = True

            if is_model:
                config: ConfigModel = ConfigModel.from_yaml(yaml=yaml_models, name=asset_name)
                config.apply(
                    game_data_dir=gamedata_dir,
                    output_dir=asset_output_subdir,
                )
            else:
                config: ConfigTexture = ConfigTexture.from_yaml(yaml=yaml_textures, name=asset_name)
                config.apply(
                    config_path=asset.parent,
                    game_data_dir=gamedata_dir,
                    output_dir=asset_output_subdir,
                    asset_name=asset_name
                )

        except Exception:
            info(asset_relative_path, status=InfoStatus.ERROR, rewrite=info_written)
            raise

        info(asset_relative_path, status=InfoStatus.DONE)