namespace KSP_PBR_Patcher.Model.ModelOperations;

public class OperationRenameTransform : OperationBase
{
    public static string OperationName => "rename_transform";

    public required string Transform { get; set; }
    public required string NewName { get; set; }

    public override void Apply(MuFile muFile, string gameDataPath)
    {
        List<MuTransform> transforms = muFile.GetTransforms(Transform);
        if (transforms.Count == 0)
        {
            throw new ArgumentException($"No transforms found with name {Transform}");
        }

        foreach (MuTransform transform in transforms)
        {
            transform.Name = NewName;
        }
    }
}