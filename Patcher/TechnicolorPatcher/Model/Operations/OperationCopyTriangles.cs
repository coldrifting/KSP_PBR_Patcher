using TechnicolorPatcher.Types;
using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Model.Operations;

[YamlSerializable]
public class OperationCopyTriangles : OperationBase
{
    public static string OperationName => "copy_triangles";

    public required string Transform { get; set; }
    public required string Triangles { get; set; }
    
    // Leave value out to copy triangles to end of mesh data
    public string? Destination { get; set; }

    public override void Apply(MuFile muFile, string gameDataPath)
    {
        List<MuTransform> transforms = muFile.GetTransforms(Transform);
        if (transforms.Count == 0)
        {
            throw new ArgumentException($"No transforms found with name {Transform}");
        }

        MuTransform? destTransform;
        if (Destination is not null)
        {
            List<MuTransform> destTransforms = muFile.GetTransforms(Destination);
            if (destTransforms.Count == 0)
            {
                throw new ArgumentException($"No transforms found with name {Destination}");
            }
            
            destTransform = destTransforms[0];
        }
        else
        {
            destTransform = null;
        }
        
        List<int> trianglesList = ListParse.ToIntList(Triangles);
        
        muFile.CopyTriangles(transforms[0], destTransform, trianglesList);
    }
}