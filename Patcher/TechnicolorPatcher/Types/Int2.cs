using YamlDotNet.Core;
using YamlDotNet.Core.Events;
using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Types;

[YamlSerializable]
public struct Int2(int x, int y)
{
    public int X { get; set; } = x;
    public int Y { get; set; } = y;
}

public class Int2Deserializer : INodeDeserializer
{
    public bool Deserialize(
        IParser reader,
        Type expectedType,
        Func<IParser, Type, object?> nestedObjectDeserializer,
        out object? value,
        ObjectDeserializer rootDeserializer)
    {
        if (expectedType != typeof(Int2))
        {
            value = null;
            return false;
        }

        int x, y;
        switch (reader.Current)
        {
            case MappingStart:
                reader.Consume<MappingStart>();
                Dictionary<string, int> values = new();
                
                string k1 = reader.Consume<Scalar>().Value;
                int v1 = int.Parse(reader.Consume<Scalar>().Value);

                values[k1] = v1;
                
                string k2 = reader.Consume<Scalar>().Value;
                int v2 = int.Parse(reader.Consume<Scalar>().Value);

                values[k2] = v2;
                reader.Consume<MappingEnd>();

                if (!values.TryGetValue("x", out int value1))
                {
                    throw new YamlException($"{reader.Current.Start}: Missing required parameter x");
                }

                if (!values.TryGetValue("y", out int value2))
                {
                    throw new YamlException($"{reader.Current.Start}: Missing required parameter y");
                }
                
                x = value1;
                y = value2;

                break;
            
            case SequenceStart:
                reader.Consume<SequenceStart>();
                x = int.Parse(reader.Consume<Scalar>().Value);
                y = int.Parse(reader.Consume<Scalar>().Value);
                reader.Consume<SequenceEnd>();
                break;
            
            case null:
                throw new YamlException("Unexpected node type");
            
            default:
                throw new YamlException($"{reader.Current.Start}: Unexpected node type");
        }
        
        value = new Int2(x, y);

        return true;
    }
}