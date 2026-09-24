from typing import Any

from data.model.operation.base import ModelOperation
from data.model.types.core.int3 import Int3
from data.model.types.mu_file import MuFile
from data.model.types.mu_tag import MuTag
from data.model.types.transform.mesh.mesh_data import MeshData
from data.model.types.transform.mesh.mesh_data_item import MeshDataItemTriangles, MeshDataItemVertices


class ModelOperationMeshEditTrianglesRemove(ModelOperation):
    def __init__(self, transform_name: str, triangles: list[int]):
        self.transform_name = transform_name
        self.triangles = triangles

    def apply(self, mu_data: MuFile):
        source = mu_data.get_mesh(self.transform_name)
        mesh_edit_tris_remove_mesh_data(source, set(self.triangles))

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'ModelOperationMeshEditTrianglesRemove':
        return ModelOperationMeshEditTrianglesRemove(
            transform_name = yaml['transform_name'],
            triangles = yaml['triangles']
        )

def mesh_edit_tris_remove_mesh_data(mesh_data: MeshData, tris: set[int]):
    remain_vertex_indices: list[bool] = []
    for i in range(mesh_data.vertex_count):
        remain_vertex_indices.append(False)

    src_triangles = mesh_data.items[MuTag.MeshTriangles].triangles
    for index, triangle in enumerate(src_triangles):
        if index not in tris:
            remain_vertex_indices[triangle.x] = True
            remain_vertex_indices[triangle.y] = True
            remain_vertex_indices[triangle.z] = True

    remain_vertex_indices_to_remove: set[int] = set()
    for i in range(len(remain_vertex_indices)):
        if not remain_vertex_indices[i]:
            remain_vertex_indices_to_remove.add(i)

    for tag in [MuTag.MeshUv, MuTag.MeshUv2, MuTag.MeshNormals, MuTag.MeshTangents, MuTag.MeshBoneWeights, MuTag.MeshVertexColors]:
        if mesh_data.items.get(tag) is not None:
            mesh_data.items[tag].delete(remain_vertex_indices_to_remove)

    reindex(mesh_data.items[MuTag.MeshVertices], mesh_data.items[MuTag.MeshTriangles], remain_vertex_indices_to_remove, tris)
    mesh_data.vertex_count = len(mesh_data.items[MuTag.MeshVertices].vertices)

def reindex(vertices: MeshDataItemVertices, triangles: MeshDataItemTriangles, vertex_indices_to_remove: set[int], tris_to_remove: set[int]):
    new_vertex_index_map: list[int] = [-1 for _ in range(0,len(vertices.vertices))]

    count = 0
    for index in range(len(vertices.vertices)):
        if index in vertex_indices_to_remove:
            continue

        new_vertex_index_map[index] = count
        count += 1

    for index in reversed(range(len(triangles.triangles))):
        triangle = triangles.triangles[index]
        new_x = new_vertex_index_map[triangle.x]
        new_y = new_vertex_index_map[triangle.y]
        new_z = new_vertex_index_map[triangle.z]
        if new_x == -1 or new_y == -1 or new_z == -1 or index in tris_to_remove:
            del triangles.triangles[index]
        else:
            triangles.triangles[index] = Int3(new_x, new_y, new_z)

    for index in reversed(range(len(vertices.vertices))):
        if index in vertex_indices_to_remove:
            del vertices.vertices[index]