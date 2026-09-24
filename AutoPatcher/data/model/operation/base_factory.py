from typing import Any

from data.model.operation.base import ModelOperation
from data.model.operation.mesh_normals_average import ModelOperationMeshEditAverageNormals
from data.model.operation.mesh_triangles_remove import ModelOperationMeshEditTrianglesRemove
from data.model.operation.mesh_triangles_transfer import ModelOperationMeshEditTrianglesTransfer
from data.model.operation.mesh_uvs_edit import ModelOperationMeshEditSetUvs
from data.model.operation.mesh_vertices_edit import ModelOperationMeshEditSetVertices
from data.model.operation.transform_duplicate import ModelOperationTransformDuplicate
from data.model.operation.transform_merge import ModelOperationTransformMerge
from data.model.operation.transform_remove import ModelOperationTransformRemove


class ModelOperationFactory:
    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'ModelOperation':
        op_type = list(yaml.keys())[0]
        match op_type:
            case "mesh_normals_average":
                return ModelOperationMeshEditAverageNormals.from_yaml(yaml[op_type])
            case "mesh_triangles_remove":
                return ModelOperationMeshEditTrianglesRemove.from_yaml(yaml[op_type])
            case "mesh_triangles_transfer":
                return ModelOperationMeshEditTrianglesTransfer.from_yaml(yaml[op_type])
            case "mesh_uvs_edit":
                return ModelOperationMeshEditSetUvs.from_yaml(yaml[op_type])
            case "mesh_vertices_edit":
                return ModelOperationMeshEditSetVertices.from_yaml(yaml[op_type])

            case "transform_duplicate":
                return ModelOperationTransformDuplicate.from_yaml(yaml[op_type])
            case "transform_merge":
                return ModelOperationTransformMerge.from_yaml(yaml[op_type])
            case "transform_remove":
                return ModelOperationTransformRemove.from_yaml(yaml[op_type])

            case _:
                raise Exception(f"Unknown yaml name: {op_type}")
