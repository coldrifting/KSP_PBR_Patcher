from pathlib import Path
from typing import Any, Tuple
import xml.etree.ElementTree as ElementTree

from PIL import Image

from data.texture.layer import Layer
from data.texture.layer_factory import LayerFactory
from utils.exceptions import ArgumentException
from utils.svg_split import split_svg


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
                 metal_alt: list[Layer],
                 export_a: bool,
                 export_m: bool,
                 export_tc: bool,
                 masks: dict[str, ElementTree.Element],
                 fills: dict[str, Image.Image]):

        self.name = name

        self.size = size

        self.color_primary = color_primary
        self.color_secondary = color_secondary
        self.diffuse = diffuse
        self.gloss = gloss
        self.metal = metal
        self.gloss_alt = gloss_alt
        self.metal_alt = metal_alt

        self.export_a = export_a
        self.export_m = export_m
        self.export_tc = export_tc

        self.masks = masks
        self.fills = fills

        self.prev_channels: dict[str, Image.Image] = {}

    def __str__(self):
        return "ConfigTexture: " + self.name

    @staticmethod
    def yaml_check_group(yaml: dict[str, Any], group_key: str):
        if yaml.get(group_key, None) is None:
            raise ArgumentException(f"Required group {group_key} is missing")

    @staticmethod
    def from_yaml(yaml: dict[str, Any], name: str, masks_file: Path) -> 'ConfigTexture':
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

        masks: dict[str, ElementTree.Element[str]] = {}
        fills: dict[str, Image.Image] = {}
        if masks_file.exists():
            masks, fills = split_svg(masks_file)

        return ConfigTexture(
            name=name,
            size=(yaml['size'][0], yaml['size'][1]),
            color_primary=color_primary,
            color_secondary=color_secondary,
            diffuse=diffuse,
            gloss=gloss,
            gloss_alt=gloss_alt,
            metal=metal,
            metal_alt=metal_alt,
            export_a=yaml.get('export_a', True),
            export_m=yaml.get('export_m', True),
            export_tc=yaml.get('export_tc', True),
            masks=masks,
            fills=fills
        )

    def apply_section(self, layers: list[Layer], mask_resource_dir: Path, game_data_dir: Path) -> Image.Image:
        if len(layers) == 0:
            raise ArgumentException("No layers specified")

        img: Image.Image = Image.new("RGB", self.size, (0, 0, 0))
        for layer in layers:
            layer.apply(size=self.size,
                        prev_channels=self.prev_channels,
                        image=img,
                        masks=self.masks,
                        fills=self.fills,
                        game_data_dir=game_data_dir)

        return img

    def apply(self,
              config_path: Path,
              game_data_dir: Path,
              output_dir: Path,
              asset_name: str) -> list[Path | None]:
        mask_resource_dir = config_path / "Resources" / asset_name

        color_primary = self.apply_section(layers=self.color_primary,
                                           mask_resource_dir=mask_resource_dir,
                                           game_data_dir=game_data_dir)
        self.prev_channels["color_primary"] = color_primary

        color_secondary = self.apply_section(layers=self.color_secondary,
                                           mask_resource_dir=mask_resource_dir,
                                           game_data_dir=game_data_dir)
        self.prev_channels["color_secondary"] = color_secondary

        diffuse = self.apply_section(layers=self.diffuse,
                                           mask_resource_dir=mask_resource_dir,
                                           game_data_dir=game_data_dir)
        self.prev_channels["diffuse"] = diffuse

        gloss = self.apply_section(layers=self.gloss,
                                           mask_resource_dir=mask_resource_dir,
                                           game_data_dir=game_data_dir)
        self.prev_channels["gloss"] = gloss

        gloss_alt = self.apply_section(layers=self.gloss_alt,
                                           mask_resource_dir=mask_resource_dir,
                                           game_data_dir=game_data_dir)
        self.prev_channels["gloss_alt"] = gloss_alt

        metal = self.apply_section(layers=self.metal,
                                           mask_resource_dir=mask_resource_dir,
                                           game_data_dir=game_data_dir)
        self.prev_channels["metal"] = metal

        metal_alt = self.apply_section(layers=self.metal_alt,
                                           mask_resource_dir=mask_resource_dir,
                                           game_data_dir=game_data_dir)
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

        output: list[Path | None] = [None, None, None]

        if self.export_a:
            albedo.save(albedo_path)
            output[0] = albedo_path

        if self.export_m:
            # Reduce size of saved metal map if all white
            if metal.convert("L").getextrema() == (255, 255):
                Image.new("RGB", (16, 16), "white").save(metal_path)
            else:
                metal.save(metal_path)
            output[1] = metal_path

        if self.export_tc:
            tc.save(tc_path)
            output[2] = tc_path

        return output
