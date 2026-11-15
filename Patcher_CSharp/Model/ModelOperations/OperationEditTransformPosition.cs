using System.Numerics;

namespace KSP_PBR_Patcher.Model.ModelOperations;

public class OperationEditTransformPosition : OperationBase
{
    public static string OperationName => "edit_transform_position";

    public required string Transform { get; set; }
    public Vector3 Position { get; set; }
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
            transform.Position = new Vector3(
                (Absolute ? 0 : transform.Position.X) + Position.X, 
                (Absolute ? 0 : transform.Position.Y) + Position.Y, 
                (Absolute ? 0 : transform.Position.Z) + Position.Z);
        }
    }
}