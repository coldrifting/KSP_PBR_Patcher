from pathlib import Path
from typing import Any, Tuple

from PIL import Image

from data.texture.layer.base import Layer
from data.texture.layer.base_factory import LayerFactory
from utils.exceptions import ArgumentException


class ConfigTexture:
    def __init__(self,
                 name: str,
                 size: Tuple[int, int],
                 color_primary: list[Layer],
                 color_secondary: list[Layer],
                 diffuse: list[Layer],
                 gloss: list[Layer],
                 metal: list[Layer],
                 gloss_alt: list[Layer],
                 metal_alt: list[Layer]):

        self.name = name

        self.size = size

        self.color_primary = color_primary
        self.color_secondary = color_secondary
        self.diffuse = diffuse
        self.gloss = gloss
        self.metal = metal
        self.gloss_alt = gloss_alt
        self.metal_alt = metal_alt

        self.prev_channels: dict[str, Image.Image] = {}

    def __str__(self):
        return "ConfigTexture: " + self.name

    @staticmethod
    def yaml_check_group(yaml: dict[str, Any], group_key: str):
        if yaml.get(group_key, None) is None:
            raise ArgumentException(f"Required group {group_key} is missing")

    @staticmethod
    def from_yaml(yaml: dict[str, Any], name: str) -> 'ConfigTexture':
        ConfigTexture.yaml_check_group(yaml, 'color_primary')
        ConfigTexture.yaml_check_group(yaml, 'color_secondary')
        ConfigTexture.yaml_check_group(yaml, 'diffuse')
        ConfigTexture.yaml_check_group(yaml, 'gloss')
        ConfigTexture.yaml_check_group(yaml, 'gloss_alt')
        ConfigTexture.yaml_check_group(yaml, 'metal')
        ConfigTexture.yaml_check_group(yaml, 'metal_alt')

        color_primary = [LayerFactory.from_yaml(x, 'color_primary') for x in yaml['color_primary']]
        color_secondary = [LayerFactory.from_yaml(x, 'color_secondary') for x in yaml['color_secondary']]
        diffuse = [LayerFactory.from_yaml(x, 'diffuse') for x in yaml['diffuse']]
        gloss = [LayerFactory.from_yaml(x, 'gloss') for x in yaml['gloss']]
        gloss_alt = [LayerFactory.from_yaml(x, 'gloss_alt') for x in yaml['gloss_alt']]
        metal = [LayerFactory.from_yaml(x, 'metal') for x in yaml['metal']]
        metal_alt = [LayerFactory.from_yaml(x, 'metal_alt') for x in yaml['metal_alt']]

        return ConfigTexture(
            name=name,
            size=(yaml['size'][0], yaml['size'][1]),
            color_primary=color_primary,
            color_secondary=color_secondary,
            diffuse=diffuse,
            gloss=gloss,
            gloss_alt=gloss_alt,
            metal=metal,
            metal_alt=metal_alt
        )

    def apply_section(self, layers: list[Layer], config_path: Path, game_data_dir: Path) -> Image.Image:
        if len(layers) == 0:
            raise ArgumentException("No layers specified")

        img: Image.Image = Image.new("RGB", self.size, (0, 0, 0))
        for layer in layers:
            layer.apply(self.size, self.prev_channels, img, config_path, game_data_dir)

        return img

    def apply(self, config_path: Path, game_data_dir: Path, output_dir: Path, asset_name: str):
        color_primary = self.apply_section(self.color_primary, config_path, game_data_dir)
        self.prev_channels["color_primary"] = color_primary

        color_secondary = self.apply_section(self.color_secondary, config_path, game_data_dir)
        self.prev_channels["color_secondary"] = color_secondary

        diffuse = self.apply_section(self.diffuse, config_path, game_data_dir)
        self.prev_channels["diffuse"] = diffuse

        gloss = self.apply_section(self.gloss, config_path, game_data_dir)
        self.prev_channels["gloss"] = gloss

        gloss_alt = self.apply_section(self.gloss_alt, config_path, game_data_dir)
        self.prev_channels["gloss_alt"] = gloss_alt

        metal = self.apply_section(self.metal, config_path, game_data_dir)
        self.prev_channels["metal"] = metal

        metal_alt = self.apply_section(self.metal_alt, config_path, game_data_dir)
        self.prev_channels["metal_alt"] = metal_alt

        # Pack channels
        albedo_r, albedo_g, albedo_b = diffuse.split()
        albedo_a = gloss.getchannel("R")
        albedo = Image.merge("RGBA", (albedo_r, albedo_g, albedo_b, albedo_a))

        tc_r = color_primary.getchannel("R")
        tc_g = color_secondary.getchannel("G")
        tc_b = gloss_alt.getchannel("B")
        tc_a = metal_alt.getchannel("R")
        tc = Image.merge("RGBA", (tc_r, tc_g, tc_b, tc_a))

        output_dir.mkdir(parents=True, exist_ok=True)

        albedo_path = Path(output_dir / Path(asset_name + "-a.png"))
        metal_path = Path(output_dir / Path(asset_name + "-m.png"))
        tc_path = Path(output_dir / Path(asset_name + "-tc.png"))

        albedo.save(albedo_path)
        metal.save(metal_path)
        tc.save(tc_path)
