using TechnicolorPatcher.Model.Tags;
using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Model.Operations;

[YamlSerializable]
public class OperationRemoveMaterials : OperationBase
{
    public static string OperationName => "remove_materials";

    public required List<string> Materials { get; set; }

    public override void Apply(MuFile muFile, string gameDataPath)
    {
        foreach (string material in Materials)
        {
            RemoveMaterial(muFile, material);
        }
    }

    private void RemoveMaterial(MuFile muFile, string materialName)
    {
        int materialIndex = muFile.GetMaterialIndex(materialName);
        if (materialIndex == -1)
        {
            throw new ArgumentException($"Material not found in file: {materialName}");
        }

        var transforms = muFile.GetTransforms(null, [MuTag.MeshRenderer, MuTag.SkinnedMeshRenderer]);
        foreach (var transform in transforms)
        {
            var transformMaterialIndex = transform.GetMaterialIndex();
            if (transformMaterialIndex == materialIndex)
            {
                throw new ArgumentException(
                    $"Cannot remove material {materialName}: Transform with name {transform.Name} currently references it");
            }

            if (transformMaterialIndex > materialIndex)
            {
                transform.SetMaterialIndex(transformMaterialIndex - 1);
            }
        }
        
        muFile.Materials.RemoveAt(materialIndex);
    }
}