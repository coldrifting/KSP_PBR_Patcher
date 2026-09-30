from pathlib import Path

import yaml

from data.texture.config_texture import ConfigTexture
from utils.info_status import InfoStatus
from utils.printing import header, info


def patch_textures(patch_data_texture_dir: Path, output_mod_asset_dir: Path, gamedata_dir: Path, texconv_path: Path | None):
    header("Processing textures...")
    for asset in patch_data_texture_dir.glob("**/*.yaml"):
        asset_name = asset.name.rstrip(".yaml")
        asset_sub_path = asset.parent.parent.relative_to(patch_data_texture_dir)
        asset_output_subdir = output_mod_asset_dir / asset_sub_path
        asset_relative_path = str(Path(asset_sub_path) / Path(asset_name))

        info(asset_relative_path, rewrite=False)

        try:
            with open(asset) as f:
                yaml_dict = yaml.safe_load(f)

                config: ConfigTexture = ConfigTexture.from_yaml(yaml=yaml_dict, name=asset_name)
                output_textures = config.apply(
                    config_path=asset.parent,
                    game_data_dir=gamedata_dir,
                    output_dir=asset_output_subdir,
                    asset_name=asset_name
                )

                if texconv_path is not None:
                    # Lazy load texconv modules
                    from texconv import Texconv, FileOptions, FormatOptions, Format

                    for texture in output_textures:
                        texconv_settings = Texconv(texconv_path,
                                                   FileOptions(output=texture.parent, overwrite=True),
                                                   FormatOptions(format=Format.DXGI_FORMAT_BC7_UNORM))

                        texconv_settings.run(texture)
                        texture.unlink()

        except Exception:
            info(asset_relative_path, status=InfoStatus.ERROR)
            raise

        info(asset_relative_path, status=InfoStatus.DONE)
