using System.Numerics;
using KSP_PBR_Patcher.Model.IO;
using KSP_PBR_Patcher.Model.Tags;

namespace KSP_PBR_Patcher.Model.Components.Material;

public class PropertyTexture : IProperty
{
    public required string Name { get; set; }
    public int TextureIndex { get; set; }
    public Vector2 TextureScale { get; set; } = new Vector2(1.0f, 1.0f);
    public Vector2 TextureOffset { get; set; } = new Vector2(0, 0);

    public static PropertyTexture Read(MuReader reader, string name)
    {
        int textureIndex = reader.ReadInt32();
        Vector2 textureScale = reader.ReadVec2();
        Vector2 textureOffset = reader.ReadVec2();

        return new PropertyTexture
        {
            Name = name,
            TextureIndex = textureIndex,
            TextureScale = textureScale,
            TextureOffset = textureOffset
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        writer.Write(Name);
        writer.Write((int)MaterialPropertyTag.Texture);
        writer.Write(TextureIndex);
        writer.Write(TextureScale);
        writer.Write(TextureOffset);
    }

    public IProperty Clone()
    {
        return new PropertyTexture
        {
            Name = Name,
            TextureIndex = TextureIndex,
            TextureScale = TextureScale,
            TextureOffset = TextureOffset
        };
    }
}