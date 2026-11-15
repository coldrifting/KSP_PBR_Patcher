namespace KSP_PBR_Patcher.Model.ModelOperations;

public class OperationCopyTransform : OperationBase
{
    public static string OperationName => "copy_transform";

    public required string Transform { get; set; }
    public required string NewName { get; set; }
    
    // Optionally copy from another model file entirely
    public string? Model { get; set; }

    public override void Apply(MuFile muFile, string gameDataPath)
    {
        if (Model is null)
        {
            List<MuTransform> transforms = muFile.GetTransforms(Transform);
            if (transforms.Count == 0)
            {
                throw new ArgumentException($"No transforms found with name {Transform}");
            }
            
            muFile.CopyTransform(transforms[0], gameDataPath);
        }
        else
        {
            muFile.CopyTransform(Transform, NewName, Model, gameDataPath);
        }
        
    }
}