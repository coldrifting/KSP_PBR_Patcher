from copy import deepcopy
from pathlib import Path
from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from data.model.types.material.material_property import MaterialProperty, MaterialPropertyTexture
from data.model.types.tag.tag_mu import MuTag
from utils.exceptions import ArgumentException
from utils.yaml_load import get_yaml_parameter


class OperationCopyTransform(Operation):
    def __init__(self, transform: str, new_name: str, model: str | None):
        self.transform = transform
        self.new_name = new_name
        self.model = model

    def apply(self, mu_data: MuData, game_data_dir: Path):
        if self.model is None:
            mu_data.copy_transform(self.transform, self.new_name)
            return

        input_file = MuData.from_file(game_data_dir / Path(self.model).with_suffix(".mu"))
        transforms = input_file.get_transforms(self.transform)
        if len(transforms) != 1:
            raise ArgumentException(f"Expected exactly 1 transform, got {len(transforms)} instead")

        if transforms[0].data is not None and transforms[0].data.get(MuTag.MeshRenderer, None) is not None:
            renderer = transforms[0][MuTag.MeshRenderer]

            material = deepcopy(input_file.materials[renderer.material_index])

            for prop in material.properties:
                if isinstance(prop, MaterialPropertyTexture):
                    texture = input_file.textures[prop.index]
                    mu_data.textures.append(texture)
                    prop.index = len(mu_data.textures) - 1

            mu_data.materials.append(material)
            renderer.material_index = len(mu_data.materials) - 1

        mu_data.root_transform.children.append(transforms[0])


    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationCopyTransform':
        transform = get_yaml_parameter(yaml, "transform", str)
        new_name = get_yaml_parameter(yaml, "new_name", str)

        model = yaml.get("model", None)

        return OperationCopyTransform(
            transform=transform,
            new_name=new_name,
            model=model)
