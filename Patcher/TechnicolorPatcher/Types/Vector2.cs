using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Types;

[YamlSerializable]
public struct Vector2(float x, float y)
{
    public float X { get; set; } = x;
    public float Y { get; set; } = y;
}