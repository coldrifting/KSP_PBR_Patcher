using KSP_PBR_Patcher.Types;

namespace KSP_PBR_Patcher.Model.ModelOperations;

public class OperationRemoveTriangles : OperationBase
{
    public static string OperationName => "remove_triangles";

    public required string Transform { get; set; }
    public required string Triangles { get; set; }

    public override void Apply(MuFile muFile, string gameDataPath)
    {
        List<MuTransform> transforms = muFile.GetTransforms(Transform);
        if (transforms.Count == 0)
        {
            throw new ArgumentException($"No transforms found with name {Transform}");
        }
        
        List<int> trianglesList = ListParse.ToIntList(Triangles);

        MuFile.RemoveTriangles(transforms[0], trianglesList);
    }
}