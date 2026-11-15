using System.Numerics;
using KSP_PBR_Patcher.Model.IO;
using KSP_PBR_Patcher.Model.Tags;

namespace KSP_PBR_Patcher.Model.Components.Material;

public class PropertyVector : IProperty
{
    public required string Name { get; set; }
    public Vector4 Vector { get; set; }
    
    public static PropertyVector Read(MuReader reader, string name)
    {
        Vector4 vector = reader.ReadVec4();

        return new PropertyVector
        {
            Name = name,
            Vector = vector
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        writer.Write(Name);
        writer.Write((int)MaterialPropertyTag.Vector);
        writer.Write(Vector);
    }

    public IProperty Clone()
    {
        return new PropertyVector
        {
            Name = Name,
            Vector = Vector
        };
    }
}