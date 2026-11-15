using System.Numerics;
using KSP_PBR_Patcher.Model.Components;
using KSP_PBR_Patcher.Model.Tags;

namespace KSP_PBR_Patcher.Model.ModelOperations;

public class OperationEditMeshVertices : OperationBase
{
    public static string OperationName => "edit_mesh_vertices";

    public required string Transform { get; set; }
    public required Dictionary<int, Vector3> Vertices { get; set; }

    public override void Apply(MuFile muFile, string gameDataPath)
    {
        List<MuTransform> transforms = muFile.GetTransforms(Transform, MuTag.MeshFilter);
        if (transforms.Count == 0)
        {
            throw new ArgumentException($"No mesh-data-containing transforms were found with the name {Transform}");
        }

        foreach (MuTransform transform in transforms)
        {
            MuComponentMesh mesh = (MuComponentMesh)transform[MuTag.MeshFilter];

            foreach ((int index, Vector3 position) in Vertices)
            {
                mesh.VertexData[index].Position = position;
            }
        }
    }
}