using TechnicolorPatcher.Model.IO;
using TechnicolorPatcher.Model.Tags;

namespace TechnicolorPatcher.Model.Components.Material;

public class PropertyFloat3 : IProperty
{
    public required string Name { get; set; }
    public float Value { get; set; }
    
    public static PropertyFloat3 Read(MuReader reader, string name)
    {
        float value = reader.ReadSingle();

        return new PropertyFloat3
        {
            Name = name,
            Value = value
        };
    }

    public void Write(BinaryWriter writer)
    {
        writer.Write(Name);
        writer.Write((int)MaterialPropertyTag.Float3);
        writer.Write(Value);
    }

    public IProperty Clone()
    {
        return new PropertyFloat3
        {
            Name = Name,
            Value = Value
        };
    }
}