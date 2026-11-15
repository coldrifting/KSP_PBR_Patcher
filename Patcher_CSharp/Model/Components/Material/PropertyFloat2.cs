using KSP_PBR_Patcher.Model.IO;
using KSP_PBR_Patcher.Model.Tags;

namespace KSP_PBR_Patcher.Model.Components.Material;

public class PropertyFloat2 : IProperty
{
    public required string Name { get; set; }
    public float Value { get; set; }
    
    public static PropertyFloat2 Read(MuReader reader, string name)
    {
        float value = reader.ReadSingle();

        return new PropertyFloat2
        {
            Name = name,
            Value = value
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        writer.Write(Name);
        writer.Write((int)MaterialPropertyTag.Float2);
        writer.Write(Value);
    }

    public IProperty Clone()
    {
        return new PropertyFloat2
        {
            Name = Name,
            Value = Value
        };
    }
}