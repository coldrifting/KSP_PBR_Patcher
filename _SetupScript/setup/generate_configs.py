from pathlib import Path

import yaml

from data.material.config_patch import ConfigPatch
from utils.terminal_colors import header, info, TerminalColors, InfoStatus


def generate_material_configs(input_material_dir: Path, output_material_dir: Path):
    header("Generating material configs...")
    for material_file in input_material_dir.glob("**/*.yaml"):
        with open(material_file, "r") as material_file_text_in:
            output_material_relative_path = material_file.relative_to(input_material_dir)
            output_material_file = Path(output_material_dir / output_material_relative_path).with_suffix(".cfg")
            output_material_file.parent.mkdir(parents=True, exist_ok=True)

            printable_name = str(Path("Materials") / output_material_relative_path)
            info(printable_name)

            yaml_dict = yaml.safe_load(material_file_text_in)
            config: ConfigPatch = ConfigPatch.from_yaml(yaml=yaml_dict)
            output_material_file_text = config.write()

            with open(output_material_file, "w") as material_file_text_out:
                material_file_text_out.write(output_material_file_text)

            info(printable_name, status=InfoStatus.DONE)
