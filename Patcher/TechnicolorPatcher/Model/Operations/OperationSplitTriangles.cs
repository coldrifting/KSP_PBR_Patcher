using TechnicolorPatcher.Model.Components;
using TechnicolorPatcher.Model.Tags;
using TechnicolorPatcher.Types;
using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Model.Operations;

[YamlSerializable]
public class OperationSplitTriangles : OperationBase
{
    public static string OperationName => "split_triangles";

    public required string Transform { get; set; }
    public required string Triangles { get; set; }
    
    // Leave value out to separate triangles inside a transform and move them to the end of the mesh data
    public string? Destination { get; set; }

    public override void Apply(MuFile muFile, string gameDataPath)
    {
        List<MuTransform> transforms = muFile.GetTransforms(Transform);
        if (transforms.Count == 0)
        {
            throw new ArgumentException($"No transforms found with name {Transform}");
        }
        
        List<int> trianglesList = ListParse.ToIntList(Triangles);

        if (Destination is null)
        {
            muFile.CopyTriangles(transforms[0], null, trianglesList);
            MuFile.RemoveTriangles(transforms[0], trianglesList);
            return;
        }
        
        List<MuTransform> destinations = muFile.GetTransforms(Destination);
        MuTransform destination;
        if (destinations.Count == 0)
        {
            MuTransform newTransform = muFile.CopyTransform(transforms[0], Destination);
            MuComponentMesh destMesh = (MuComponentMesh)newTransform[MuTag.MeshFilter];
            destMesh.VertexData = [];
            destMesh.Triangles = [];

            destination = newTransform;
        }
        else
        {
            destination = destinations[0];
        }

        muFile.CopyTriangles(transforms[0], destination, trianglesList);
        MuFile.RemoveTriangles(transforms[0], trianglesList);
    }
}