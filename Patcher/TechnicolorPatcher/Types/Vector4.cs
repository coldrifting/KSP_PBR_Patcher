using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Types;

[YamlSerializable]
public struct Vector4(float x, float y, float z, float w)
{
    public float X { get; set; } = x;
    public float Y { get; set; } = y;
    public float Z { get; set; } = z;
    public float W { get; set; } = w;
}