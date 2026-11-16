using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Types;

[YamlSerializable]
public struct Int3(int x, int y, int z)
{
    public int X { get; set; } = x;
    public int Y { get; set; } = y;
    public int Z { get; set; } = z;
}