using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Model.Operations;

[YamlSerializable]
public class OperationRemoveTransforms : OperationBase
{
    public static string OperationName => "remove_transforms";

    public required List<string> Transforms { get; set; }

    public override void Apply(MuFile muFile, string gameDataPath)
    {
        foreach (string transform in Transforms)
        {
            RemoveTransform(muFile, transform);
        }
    }

    private void RemoveTransform(MuFile muFile, string transformName)
    {
        if (muFile.RootTransform.Name == transformName)
        {
            throw new ArgumentException("Cannot remove root transform");
        }

        List<MuTransform> transforms = muFile.GetTransforms(transformName);
        if (transforms.Count == 0)
        {
            throw new ArgumentException($"No transforms found with name {transformName}");
        }
        
        Queue<List<MuTransform>> queue = new();
        queue.Enqueue(muFile.RootTransform.Children);
        
        int transformsRemaining = transforms.Count;

        while (queue.Count > 0)
        {
            List<MuTransform> muTransforms = queue.Dequeue();
            for (int i = muTransforms.Count - 1; i >= 0; i--)
            {
                foreach (MuTransform transform in transforms)
                {
                    if (muTransforms[i] == transform)
                    {
                        muTransforms.RemoveAt(i);
                        transformsRemaining--;
                        if (transformsRemaining == 0)
                        {
                            return;
                        }
                    }
                }

                queue.Enqueue(muTransforms[i].Children);
            }
        }
    }
}