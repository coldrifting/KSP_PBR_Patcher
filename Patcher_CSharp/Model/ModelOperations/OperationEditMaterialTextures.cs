using KSP_PBR_Patcher.Model.Components.Material;

namespace KSP_PBR_Patcher.Model.ModelOperations;

public class OperationEditMaterialTextures : OperationBase
{
    public static string OperationName => "edit_material_textures";
    
    public required string Material { get; set; }
    public string? MainTex { get; set; }
    public string? BumpMap { get; set; }
    public string? Emissive { get; set; }
    public string? MetalMap { get; set; }
    public string? TeamColorMap { get; set; }

    public override void Apply(MuFile muFile, string gameDataPath)
    {
        Material material = muFile.GetMaterial(Material);
        PropertyTexture mainTex = (PropertyTexture)material.Properties.First(s => s.Name == "_MainTex");
        if (MainTex is not null)
        {
            muFile.EditTextureMap(material, "_MainTex", Path.GetFileNameWithoutExtension(MainTex), mainTex.TextureScale, mainTex.TextureOffset);
        }
        
        if (BumpMap is not null)
        {
            muFile.EditTextureMap(material, "_BumpMap", Path.GetFileNameWithoutExtension(BumpMap), mainTex.TextureScale, mainTex.TextureOffset);
        }
        
        if (Emissive is not null)
        {
            muFile.EditTextureMap(material, "_Emissive", Path.GetFileNameWithoutExtension(Emissive), mainTex.TextureScale, mainTex.TextureOffset);
        }
        
        if (MetalMap is not null)
        {
            muFile.EditTextureMap(material, "_MetalMap", Path.GetFileNameWithoutExtension(MetalMap), mainTex.TextureScale, mainTex.TextureOffset);
        }
        
        if (TeamColorMap is not null)
        {
            muFile.EditTextureMap(material, "_TeamColorMap", Path.GetFileNameWithoutExtension(TeamColorMap), mainTex.TextureScale, mainTex.TextureOffset);
        }
    }
}