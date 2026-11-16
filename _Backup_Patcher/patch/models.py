from pathlib import Path

import yaml

from data.model.config_model import ConfigModel
from utils.info_status import InfoStatus
from utils.printing import header, info
from utils.terminal_colors import TerminalColors


def patch_models(patch_data_model_dir: Path,
                 output_mod_asset_dir: Path,
                 output_root_dir: Path,
                 gamedata_dir: Path,
                 single_model_path: Path | None):
    header("Processing models...")
    assets: list[Path] = []
    if single_model_path is not None:
        assets.append(single_model_path.with_suffix(".yaml"))
    else:
        assets = list(patch_data_model_dir.glob("**/*.yaml"))

    for asset in assets:
        asset_name = asset.name.removesuffix(".yaml")
        asset_sub_path = str(asset.parent.relative_to(patch_data_model_dir)).removesuffix(".yaml")
        asset_relative_path = str(Path(asset_sub_path) / Path(asset_name))

        info_text = str(asset_relative_path)
        info(info_text, rewrite=False)

        try:
            with open(asset) as f:
                yaml_dict = yaml.safe_load(f)

                config: ConfigModel = ConfigModel.from_yaml(yaml=yaml_dict)

                info_text = info_text + f" ({TerminalColors.CYAN}{config.part}{TerminalColors.ENDC})"
                info(info_text)

                if (config.dlc == "MakingHistory" and not (gamedata_dir / "SquadExpansion" / "MakingHistory").exists()) or (config.dlc == "BreakingGround" and not (gamedata_dir / "SquadExpansion" / "Serenity").exists()):
                    info(info_text + f" {TerminalColors.YELLOW}(Skipping...){TerminalColors.ENDC}", status=InfoStatus.WARN)
                    continue

                config.apply(
                    game_data_dir=gamedata_dir,
                    output_root_dir=output_root_dir,
                    asset_output_dir=(output_mod_asset_dir / asset_sub_path)
                )

        except Exception:
            info(info_text, status=InfoStatus.ERROR)
            raise

        info(info_text, status=InfoStatus.DONE)
