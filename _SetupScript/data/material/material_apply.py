from typing import Any

from utils.exceptions import ArgumentException


class ConfigPartMaterialApplication:
    def __init__(self,
                 zone: str,
                 name: str,
                 target_material: str,
                 target_transforms: list[str] | None = None,
                 ignore_transforms: list[str] | None = None):
        self.zone = zone
        self.name = name
        self.target_material = target_material
        self.target_transforms = target_transforms
        self.ignore_transforms = ignore_transforms

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'ConfigPartMaterialApplication':
        zone: str | None = yaml.get("zone", None)
        if zone is None:
            raise ArgumentException("Missing zone value for material application")

        name: str | None = yaml.get("name", None)
        if name is None:
            raise ArgumentException("Missing name value for material application")

        target_material: str | None = yaml.get("target_material", None)
        if target_material is None:
            raise ArgumentException("Missing target_material value for material application")

        target_transforms: list[str] | None = yaml.get("target_transforms", None)
        ignore_transforms: list[str] | None = yaml.get("ignore_transforms", None)

        return ConfigPartMaterialApplication(
            zone=zone,
            name=name,
            target_material=target_material,
            target_transforms=target_transforms,
            ignore_transforms=ignore_transforms
        )
