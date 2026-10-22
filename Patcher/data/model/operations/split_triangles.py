from typing import Any

from data.model.mu_data import MuData
from data.model.operations.operation import Operation
from data.model.types.tag.tag_mu import MuTag
from utils.string_to_range import string_to_range
from utils.yaml_load import get_yaml_parameter


class OperationSplitTriangles(Operation):
    def __init__(self, transform: str, destination: str | None, triangles: list[int]):
        self.transform = transform
        self.destination = destination
        self.triangles = triangles

    def apply(self, mu_data: MuData):
        if self.destination is None:
            mu_data.copy_triangles(self.transform, self.destination, self.triangles)
            mu_data.remove_triangles(self.transform, self.triangles)
            return

        destinations = mu_data.get_transforms(self.destination)
        if len(destinations) < 1:
            new_transform = mu_data.copy_transform(transform_name=self.transform, new_name=self.destination)
            mesh = new_transform[MuTag.MeshFilter]
            mesh.vertex_data.clear()
            mesh.triangles.clear()

        mu_data.copy_triangles(self.transform, self.destination, self.triangles)

        if len(destinations) >= 1:
            mu_data.remove_triangles(self.transform, self.triangles)
        else:
            mu_data.remove_triangles(self.transform, self.triangles)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'OperationSplitTriangles':
        transform = get_yaml_parameter(yaml, "transform", str)
        destination = yaml.get("destination", None)

        triangles_range = get_yaml_parameter(yaml, "triangles", str)
        triangles = string_to_range(triangles_range)

        return OperationSplitTriangles(
            transform=transform,
            destination=destination,
            triangles=triangles)
