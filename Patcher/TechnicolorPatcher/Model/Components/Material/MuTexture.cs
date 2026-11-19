using TechnicolorPatcher.Model.IO;

namespace TechnicolorPatcher.Model.Components.Material;

public class MuTexture
{
    public required string Name { get; set; }
    public bool IsNormalMap { get; set; }

    public static MuTexture Read(MuReader reader)
    {
        string name = reader.ReadString();
        int isNormalMap = reader.ReadInt32();

        return new MuTexture
        {
            Name = name,
            IsNormalMap = isNormalMap != 0,
        };
    }

    public void Write(BinaryWriter writer)
    {
        writer.Write(Name);
        int isNormalMap = IsNormalMap ? 1 : 0;
        writer.Write(isNormalMap);
    }
}