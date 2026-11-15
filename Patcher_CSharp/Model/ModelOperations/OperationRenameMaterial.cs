using KSP_PBR_Patcher.Model.Components.Material;

namespace KSP_PBR_Patcher.Model.ModelOperations;

public class OperationRenameMaterial : OperationBase
{
    public static string OperationName => "rename_material";

    public required string Material { get; set; }
    public required string NewName { get; set; }

    public override void Apply(MuFile muFile, string gameDataPath)
    {
        Material material = muFile.GetMaterial(Material);
        material.Name = NewName;
    }
}