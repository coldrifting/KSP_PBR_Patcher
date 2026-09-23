from pathlib import Path

from texconv import Texconv, FileOptions, FormatOptions, Format

from utils.terminal_colors import header, info, TerminalColors, InfoStatus


def compress(output_asset_dir: Path, texconv_path: Path):
    header("Compressing textures...")
    for texture in Path(output_asset_dir).glob("**/*.png"):

        current_item = Path("Assets") / texture.relative_to(output_asset_dir)

        info(current_item)

        try:
            texconv_settings = Texconv(texconv_path,
                                       FileOptions(output=texture.parent, overwrite=True),
                                       FormatOptions(format=Format.DXGI_FORMAT_BC7_UNORM))
            texconv_settings.run(texture)

            texture.unlink()
        except Exception:
            info(current_item, status=InfoStatus.ERROR)
            raise

        info(current_item, status=InfoStatus.DONE)
