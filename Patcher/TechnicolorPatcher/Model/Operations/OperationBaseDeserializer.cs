using YamlDotNet.Core;
using YamlDotNet.Core.Events;
using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Model.Operations;

[YamlSerializable]
public class OperationBaseDeserializer : INodeDeserializer
{
    private readonly Dictionary<string, Type> _typeMap = new()
    {
        [OperationCopyMaterial.OperationName] = typeof(OperationCopyMaterial),
        [OperationCopyTransform.OperationName] = typeof(OperationCopyTransform),
        [OperationCopyTriangles.OperationName] = typeof(OperationCopyTriangles),
        [OperationEditMaterialShader.OperationName] = typeof(OperationEditMaterialShader),
        [OperationEditMaterialTextures.OperationName] = typeof(OperationEditMaterialTextures),
        [OperationEditMeshNormals.OperationName] = typeof(OperationEditMeshNormals),
        [OperationEditMeshNormalsAverage.OperationName] = typeof(OperationEditMeshNormalsAverage),
        [OperationEditMeshUvs.OperationName] = typeof(OperationEditMeshUvs),
        [OperationEditMeshVertices.OperationName] = typeof(OperationEditMeshVertices),
        [OperationEditTransformPosition.OperationName] = typeof(OperationEditTransformPosition),
        [OperationEditTransformRotation.OperationName] = typeof(OperationEditTransformRotation),
        [OperationEditTransformScale.OperationName] = typeof(OperationEditTransformScale),
        [OperationRemoveMaterials.OperationName] = typeof(OperationRemoveMaterials),
        [OperationRemoveTextures.OperationName] = typeof(OperationRemoveTextures),
        [OperationRemoveTransforms.OperationName] = typeof(OperationRemoveTransforms),
        [OperationRemoveTriangles.OperationName] = typeof(OperationRemoveTriangles),
        [OperationRenameMaterial.OperationName] = typeof(OperationRenameMaterial),
        [OperationRenameTransform.OperationName] = typeof(OperationRenameTransform),
        [OperationReRoot.OperationName] = typeof(OperationReRoot),
        [OperationSetParent.OperationName] = typeof(OperationSetParent),
        [OperationSplitTriangles.OperationName] = typeof(OperationSplitTriangles),
    };

    public bool Deserialize(
        IParser reader,
        Type expectedType,
        Func<IParser, Type, object?> nestedObjectDeserializer,
        out object? value,
        ObjectDeserializer rootDeserializer)
    {
        // Only intercept when deserializing an IShape
        if (expectedType != typeof(OperationBase))
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