namespace TechnicolorPatcher.Types;

public struct BoneWeight(Int4 indices, Vector4 weights)
{
    public Int4 Indices { get; set; } = indices;
    public Vector4 Weights { get; set; } = weights;
}