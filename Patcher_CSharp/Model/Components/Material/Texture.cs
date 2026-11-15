using KSP_PBR_Patcher.Model.IO;

namespace KSP_PBR_Patcher.Model.Components.Material;

public class Texture
{
    public required string Name { get; set; }
    public bool IsNormalMap { get; set; }

    public static Texture Read(MuReader reader)
    {
        string name = reader.ReadString();
        int isNormalMap = reader.ReadInt32();

        return new Texture
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