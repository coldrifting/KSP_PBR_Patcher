using TechnicolorPatcher.Model.Components.Material;
using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Model.Operations;

[YamlSerializable]
public class OperationEditMaterialShader : OperationBase
{
    public static string OperationName => "edit_material_shader";

    public required string Material { get; set; }
    public required string Shader { get; set; }

    public override void Apply(MuFile muFile, string gameDataPath)
    {
        Material material = muFile.GetMaterial(Material);
        material.ShaderName = Shader;
        if (Shader == "Resurfaced/Standard")
        {
            PropertyTexture mainTex = (PropertyTexture)material.Properties.First(p => p.Name == "_MainTex");
            muFile.AddTextureMap(material, "_MetalMap", mainTex + "-m", mainTex.TextureScale, mainTex.TextureOffset);
        }
    }
}