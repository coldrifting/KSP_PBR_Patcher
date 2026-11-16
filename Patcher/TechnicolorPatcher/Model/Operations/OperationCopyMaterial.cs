using TechnicolorPatcher.Model.Components.Material;
using TechnicolorPatcher.Model.Tags;
using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Model.Operations;

[YamlSerializable]
public class OperationCopyMaterial : OperationBase
{
    public static string OperationName => "copy_material";

    public required string Material { get; set; }
    public required string NewName { get; set; }
    public required string[] Transforms { get; set; }

    public override void Apply(MuFile muFile, string gameDataPath)
    {
        Material material = muFile.GetMaterial(Material);
        muFile.CopyMaterial(material, NewName);

        List<MuTransform> transforms = [];
        foreach (string transformName in Transforms)
        {
            List<MuTransform> matches = muFile.GetTransforms(transformName, [MuTag.MeshRenderer, MuTag.SkinnedMeshRenderer]);
            if (matches.Count == 0)
            {
                throw new ArgumentException("Unable to find transform with name " + transformName);
            }
            transforms.AddRange(matches);
        }

        foreach (MuTransform transform in transforms)
        {
            MuFile.AssignMaterial(transform, muFile.Materials.Count - 1);
        }
    }
}