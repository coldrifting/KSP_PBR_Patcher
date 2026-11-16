using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Model.Operations;

[YamlSerializable]
public class OperationReRoot : OperationBase
{
    public static string OperationName => "reroot";

    public required string Name { get; set; }

    public override void Apply(MuFile muFile, string gameDataPath)
    {
        MuTransform subroot = new()
        {
            Name = Name
        };

        List<MuTransform> rootChildren = [];
        for (int i = muFile.RootTransform.Children.Count - 1; i >= 0; i--)
        {
            rootChildren.Add(muFile.RootTransform.Children[i]);
            muFile.RootTransform.Children.RemoveAt(i);
        }
        
        rootChildren.Reverse();
        subroot.Children = rootChildren;
        
        muFile.RootTransform.Children.Add(subroot);
    }
}