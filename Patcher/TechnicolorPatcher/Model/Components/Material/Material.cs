using TechnicolorPatcher.Types;
using TechnicolorPatcher.Model.IO;
using TechnicolorPatcher.Model.Tags;

namespace TechnicolorPatcher.Model.Components.Material;

public class Material
{
    public required string Name { get; set; }
    public required string ShaderName { get; set; }
    public required List<IProperty> Properties { get; set; }

    public static Material Read(MuReader reader)
    {
        string name = reader.ReadString();
        string shaderName;
        IProperty[] properties;
        
        if (reader.Version <= 3)
        {
            LegacyMaterialTag matType = (LegacyMaterialTag)reader.ReadInt32();
            shaderName = LegacyMaterialLookup.GetShaderName(matType);
            properties = LegacyMaterialLookup.GetProperties(matType, reader);
        }
        else
        {
            shaderName = reader.ReadString();
            int numProperties = reader.ReadInt32();
            properties = new IProperty[numProperties];
            for (int i = 0; i < properties.Length; i++)
            {
                string propName = reader.ReadString();
                MaterialPropertyTag propType = (MaterialPropertyTag)reader.ReadInt32();
                switch (propType)
                {
                    case MaterialPropertyTag.Color:
                        PropertyColor propColor = PropertyColor.Read(reader, propName);
                        properties[i] = propColor;
                        break;
                    case MaterialPropertyTag.Vector:
                        PropertyVector propVector = PropertyVector.Read(reader, propName);
                        properties[i] = propVector;
                        break;
                    case MaterialPropertyTag.Float2:
                        PropertyFloat2 propFloat2 = PropertyFloat2.Read(reader, propName);
                        properties[i] = propFloat2;
                        break;
                    case MaterialPropertyTag.Float3:
                        PropertyFloat3 propFloat3 = PropertyFloat3.Read(reader, propName);
                        properties[i] = propFloat3;
                        break;
                    case MaterialPropertyTag.Texture:
                        PropertyTexture propTexture = PropertyTexture.Read(reader, propName);
                        properties[i] = propTexture;
                        break;
                    default:
                        throw new ArgumentException("Unknown material property type");
                }
            }
        }

        return new Material
        {
            Name = name,
            ShaderName = shaderName,
            Properties = properties.ToList()
        };
    }

    public void Write(BinaryWriter writer)
    {
        writer.Write(Name);
        writer.Write(ShaderName);
        
        writer.Write(Properties.Count);
        foreach (IProperty property in Properties)
        {
            property.Write(writer);
        }
    }

    public Material Clone()
    {
        return new Material
        {
            Name = Name,
            ShaderName = ShaderName,
            Properties = Properties.Select(p => p.Clone()).ToList()
        };
    }

    public void AddOrUpdateProperty(string propName, object value)
    {
        if (Properties.All(p => p.Name != propName))
        {
            switch (value)
            {
                case float f:
                    PropertyFloat3 propF = new()
                    {
                        Name = propName,
                        Value = f
                    };
                    Properties.Add(propF);
                    break;
                case Vector4 color:
                    PropertyColor propC = new()
                    {
                        Name = propName,
                        Color = color
                    };
                    Properties.Add(propC);
                    break;
                default:
                    throw new NotSupportedException();
            }
        }
        else
        {
            IProperty prop = Properties.First(p => p.Name == propName);
            switch (prop)
            {
                case PropertyFloat3 propF when value is float f:
                    propF.Value = f;
                    break;
                case PropertyColor propC when value is Vector4 color:
                    propC.Color = color;
                    break;
                case PropertyVector propV when value is Vector4 vector:
                    propV.Vector = vector;
                    break;
                default:
                    throw new NotSupportedException();
            }
        }
    }
}