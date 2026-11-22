using YamlDotNet.Core;
using YamlDotNet.Core.Events;
using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Texture.Layers;

[YamlSerializable]
public class LayerBaseDeserializer() : INodeDeserializer
{
    private readonly Dictionary<string, Type> _typeMap = new()
    {
        [LayerBrightness.LayerName] = typeof(LayerBrightness),
        [LayerCopy.LayerName] = typeof(LayerCopy),
        [LayerCurves.LayerName] = typeof(LayerCurves),
        [LayerFill.LayerName] = typeof(LayerFill),
        [LayerSaturation.LayerName] = typeof(LayerSaturation),
    };

    public bool Deserialize(
        IParser reader,
        Type expectedType,
        Func<IParser, Type, object?> nestedObjectDeserializer,
        out object? value,
        ObjectDeserializer rootDeserializer)
    {
        // Only intercept when deserializing an IShape
        if (expectedType != typeof(LayerBase))
        {
            value = null;
            return false;
        }

        // Expect the start of a YAML mapping (e.g., "- shape_type_1:")
        reader.Consume<MappingStart>();

        // Read the wrapper key name
        string typeKey = reader.Consume<Scalar>().Value;

        if (!_typeMap.TryGetValue(typeKey, out Type? targetType))
        {
            throw new YamlException($"Invalid operation: '{typeKey}'");
        }

        // Deserialize the nested object (e.g., "a: abc") into the concrete type
        value = nestedObjectDeserializer(reader, targetType);

        // Consume the end of the outer wrapper mapping
        reader.Consume<MappingEnd>();

        return true;
    }
}