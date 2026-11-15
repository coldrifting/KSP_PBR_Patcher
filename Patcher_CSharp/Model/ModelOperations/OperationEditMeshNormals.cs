using System.Numerics;
using KSP_PBR_Patcher.Model.Components;
using KSP_PBR_Patcher.Model.Tags;

namespace KSP_PBR_Patcher.Model.ModelOperations;

public class OperationEditMeshNormals : OperationBase
{
    public static string OperationName => "edit_mesh_normals";

    public required string Transform { get; set; }
    public required Dictionary<int, Vector3> Normals { get; set; }

    public override void Apply(MuFile muFile, string gameDataPath)
    {
        List<MuTransform> transforms = muFile.GetTransforms(Transform);
        if (transforms.Count == 0)
        {
            throw new ArgumentException($"No transforms found with name {Transform}");
        }
        
        foreach (MuTransform transform in transforms)
        {
            MuComponentMesh mesh = (MuComponentMesh)transform[MuTag.MeshFilter];
            
            foreach ((int index, Vector3 normal) in Normals)
            {
                mesh.VertexData[index].Normal = normal;
            }
        }
    }
}