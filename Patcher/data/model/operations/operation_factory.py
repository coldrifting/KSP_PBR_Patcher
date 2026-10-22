from typing import Any

from data.model.operations.add_team_colors import OperationAddTeamColors
from data.model.operations.assign_material import OperationAssignMaterial
from data.model.operations.copy_material import OperationCopyMaterial
from data.model.operations.copy_transform import OperationCopyTransform
from data.model.operations.copy_triangles import OperationCopyTriangles
from data.model.operations.edit_material_shader import OperationEditMaterialShader
from data.model.operations.edit_material_textures import OperationEditMaterialTextures
from data.model.operations.edit_normals import OperationEditNormals
from data.model.operations.edit_normals_average import OperationEditNormalsAverage
from data.model.operations.edit_team_colors import OperationEditTeamColors
from data.model.operations.edit_uvs import OperationEditUvs
from data.model.operations.edit_vertices import OperationEditVertices
from data.model.operations.operation import Operation
from data.model.operations.remove_transform import OperationRemoveTransform
from data.model.operations.remove_triangles import OperationRemoveTriangles
from data.model.operations.reroot import OperationReroot
from data.model.operations.rotate_transform import OperationRotateTransform
from data.model.operations.set_parent import OperationSetParent
from data.model.operations.split_triangles import OperationSplitTriangles
from utils.exceptions import ArgumentException


class OperationFactory:
    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> Operation:
        operation = next(iter(yaml))
        data = yaml[operation]

        match operation:
            case "add_team_colors":
                return OperationAddTeamColors.from_yaml(data)
            case "assign_material":
                return OperationAssignMaterial.from_yaml(data)
            case "copy_material":
                return OperationCopyMaterial.from_yaml(data)
            case "copy_transform":
                return OperationCopyTransform.from_yaml(data)
            case "copy_triangles":
                return OperationCopyTriangles.from_yaml(data)
            case "edit_material_shader":
                return OperationEditMaterialShader.from_yaml(data)
            case "edit_material_textures":
                return OperationEditMaterialTextures.from_yaml(data)
            case "edit_normals":
                return OperationEditNormals.from_yaml(data)
            case "edit_normals_average":
                return OperationEditNormalsAverage.from_yaml(data)
            case "edit_team_colors":
                return OperationEditTeamColors.from_yaml(data)
            case "edit_uvs":
                return OperationEditUvs.from_yaml(data)
            case "edit_vertices":
                return OperationEditVertices.from_yaml(data)
            case "remove_transform":
                return OperationRemoveTransform.from_yaml(data)
            case "remove_triangles":
                return OperationRemoveTriangles.from_yaml(data)
            case "rotate_transform":
                return OperationRotateTransform.from_yaml(data)
            case "reroot":
                return OperationReroot.from_yaml(data)
            case "set_parent":
                return OperationSetParent.from_yaml(data)
            case "split_triangles":
                return OperationSplitTriangles.from_yaml(data)
            case _:
                raise ArgumentException(f"Unknown operation: {operation}")
