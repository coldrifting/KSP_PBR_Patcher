using System.Numerics;

namespace KSP_PBR_Patcher.Model.ModelOperations;

public class OperationSetParent : OperationBase
{
    public static string OperationName => "set_parent";

    public required string Parent { get; set; }
    public required List<string> Transforms { get; set; }
    public bool ResetRotAndScale { get; set; }

    public override void Apply(MuFile muFile, string gameDataPath)
    {
        if (Transforms.Contains(muFile.RootTransform.Name))
        {
            throw new ArgumentException("Cannot set root transform parent to child");
        }
        
        List<MuTransform> transforms = muFile.GetTransforms(Parent);
        if (transforms.Count == 0)
        {
            throw new ArgumentException($"No transforms found with name {Parent}");
        }

        var parent = transforms[0];
        
        var queue =  new Queue<List<MuTransform>>();
        queue.Enqueue(muFile.RootTransform.Children);

        List<MuTransform> newChildren = [];
        
        while (queue.Count > 0)
        {
            List<MuTransform> muTransforms = queue.Dequeue();
            for (int i = muTransforms.Count - 1; i >= 0; i--)
            {
                MuTransform child = muTransforms[i];
                if (Transforms.Contains(child.Name))
                {
                    newChildren.Add(child);
                    muTransforms.RemoveAt(i);
                }
                else
                {
                    queue.Enqueue(child.Children);
                }
            }
        }

        newChildren.Reverse();
        foreach (MuTransform transform in newChildren)
        {
            parent.Children.Add(transform);
        
            if (ResetRotAndScale)
            {
                OperationEditTransformScale operationScale = new()
                {
                    Transform = transform.Name,
                    Scale = Vector3.One,
                    Absolute = true
                };
                OperationEditTransformRotation operationRotate = new()
                {
                    Transform = transform.Name,
                    Rotation = Vector3.Zero,
                    Absolute = true
                };

                operationScale.Apply(muFile, gameDataPath);
                operationRotate.Apply(muFile, gameDataPath);
            }
        }
    }
}