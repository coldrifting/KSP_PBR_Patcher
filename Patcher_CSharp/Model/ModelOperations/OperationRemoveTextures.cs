using KSP_PBR_Patcher.Model.Components.Material;

namespace KSP_PBR_Patcher.Model.ModelOperations;

public class OperationRemoveTextures : OperationBase
{
    public static string OperationName => "remove_textures";

    public required List<string> Textures { get; set; }

    public override void Apply(MuFile muFile, string gameDataPath)
    {
        foreach (string texture in Textures)
        {
            RemoveTexture(muFile, texture);
        }
    }

    private void RemoveTexture(MuFile muFile, string textureName)
    {
        int textureIndex = muFile.GetTextureIndex(textureName);
        if (textureIndex == -1)
        {
            throw new ArgumentException($"Texture not found in file: {textureName}");
        }
        
        foreach (Material material in muFile.Materials)
        {
            for (int i = material.Properties.Count - 1; i >= 0; i--)
            {
                IProperty property = material.Properties[i];
                if (property is PropertyTexture textureProperty)
                {
                    if (textureProperty.TextureIndex == textureIndex)
                    {
                        material.Properties.RemoveAt(i);
                    }

                    if (textureProperty.TextureIndex > textureIndex)
                    {
                        textureProperty.TextureIndex -= 1;
                    }
                }
            }
        }
        
        muFile.Textures.RemoveAt(textureIndex);
    }
}