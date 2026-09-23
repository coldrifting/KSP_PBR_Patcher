from typing import Any

from data.model.operation.base import ModelOperation
from data.model.operation.mesh_triangles_remove import mesh_edit_tris_remove_mesh_data
from data.model.types.mu_file import MuFile
from data.model.types.mu_tag import MuTag


class ModelOperationMeshEditTrianglesTransfer(ModelOperation):
    def __init__(self, transform_name_src: str, transform_name_dst: str, triangles: list[int], create_transform: bool = False):
        self.transform_name_src = transform_name_src
        self.transform_name_dst = transform_name_dst
        self.triangles = triangles
        self.create_transform = create_transform

    def apply(self, mu_data: MuFile):
        source = mu_data.get_mesh(self.transform_name_src)
        inverse = source.clone()

        tris_all = set(range(len(inverse.items[MuTag.MeshTriangles].triangles)))
        tris_inverse = tris_all.difference(self.triangles)

        mesh_edit_tris_remove_mesh_data(source, set(self.triangles))
        mesh_edit_tris_remove_mesh_data(inverse, tris_inverse)

        if self.create_transform:
            new_transform = mu_data.clone_transform(
                self.transform_name_src,
                self.transform_name_dst,
                True
            )
            new_transform.mesh_data = inverse
            return

        dest = mu_data.get_mesh(self.transform_name_dst)
        dest.merge(inverse)

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'ModelOperationMeshEditTrianglesTransfer':
        return ModelOperationMeshEditTrianglesTransfer(
            transform_name_src = yaml['transform_name_src'],
            transform_name_dst = yaml['transform_name_dst'],
            triangles = yaml['triangles'],
            create_transform = yaml.get('create_transform', False)
        )
