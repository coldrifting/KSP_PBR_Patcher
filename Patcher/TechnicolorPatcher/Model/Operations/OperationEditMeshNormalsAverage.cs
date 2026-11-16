using TechnicolorPatcher.Types;
using TechnicolorPatcher.Model.Components;
using TechnicolorPatcher.Model.Tags;
using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Model.Operations;

[YamlSerializable]
public class OperationEditMeshNormalsAverage : OperationBase
{
    public static string OperationName => "edit_mesh_normals_average";

    public required string Transform { get; set; }
    public required List<List<int>> VertexGroups { get; set; }

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

            foreach (List<int> group in VertexGroups)
            {
                Vector3 normalSum = Vector3.Zero;

                foreach (int vertexIndex in group)
                {
                    normalSum = normalSum + (mesh.VertexData[vertexIndex].Normal ?? Vector3.Zero);
                }
                
                normalSum = normalSum / VertexGroups.Count;
                normalSum = Vector3.Normalize(normalSum);

                foreach (int vertexIndex in group)
                {
                    mesh.VertexData[vertexIndex].Normal = normalSum;
                }
            }
        }
    }
}