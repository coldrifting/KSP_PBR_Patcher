from pathlib import Path

import yaml

from data.model.config_model import ConfigModel
from utils.info_status import InfoStatus
from utils.printing import header, info


def patch_models(patch_data_model_dir: Path, output_mod_asset_dir: Path, gamedata_dir: Path):
    header("Processing models...")
    for asset in patch_data_model_dir.glob("**/*.yaml"):
        asset_name = asset.name.rstrip(".yaml")
        asset_sub_path = str(asset.parent.relative_to(patch_data_model_dir)).rstrip(".yaml")
        asset_output_subdir = output_mod_asset_dir / asset_sub_path
        asset_relative_path = str(Path(asset_sub_path) / Path(asset_name))

        info(asset_relative_path, rewrite=False)

        try:
            with open(asset) as f:
                yaml_dict = yaml.safe_load(f)

                config: ConfigModel = ConfigModel.from_yaml(yaml=yaml_dict, name=asset_name)
                config.apply(
                    game_data_dir=gamedata_dir,
                    output_dir=asset_output_subdir,
                )

        except Exception:
            info(asset_relative_path, status=InfoStatus.ERROR)
            raise

        info(asset_relative_path, status=InfoStatus.DONE)
