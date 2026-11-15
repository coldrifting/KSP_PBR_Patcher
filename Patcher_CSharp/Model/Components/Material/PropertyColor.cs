using System.Numerics;
using KSP_PBR_Patcher.Model.IO;
using KSP_PBR_Patcher.Model.Tags;

namespace KSP_PBR_Patcher.Model.Components.Material;

public class PropertyColor : IProperty
{
    public required string Name { get; set; }
    public Vector4 Color { get; set; }

    public static PropertyColor Read(MuReader reader, string name)
    {
        Vector4 color = reader.ReadVec4();

        return new PropertyColor
        {
            Name = name,
            Color = color
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        writer.Write(Name);
        writer.Write((int)MaterialPropertyTag.Color);
        writer.Write(Color);
    }

    public IProperty Clone()
    {
        return new PropertyColor
        {
            Name = Name,
            Color = Color
        };
    }
}