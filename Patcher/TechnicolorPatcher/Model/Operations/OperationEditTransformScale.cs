using TechnicolorPatcher.Types;
using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Model.Operations;

[YamlSerializable]
public class OperationEditTransformScale : OperationBase
{
    public static string OperationName => "edit_transform_scale";

    public required string Transform { get; set; }
    public required Vector3 Scale { get; set; }
    public bool Absolute { get; set; }

    public override void Apply(MuFile muFile, string gameDataPath)
    {
        List<MuTransform> transforms = muFile.GetTransforms(Transform);
        if (transforms.Count == 0)
        {
            throw new ArgumentException($"No transforms found with name {Transform}");
        }

        foreach (MuTransform transform in transforms)
        {
            transform.Scale = new Vector3(
                (Absolute ? 1 : transform.Scale.X) * Scale.X,
                (Absolute ? 1 : transform.Scale.Y) * Scale.Y,
                (Absolute ? 1 : transform.Scale.Z) * Scale.Z);
        }
    }
}