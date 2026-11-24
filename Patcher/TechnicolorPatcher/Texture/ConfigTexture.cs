using SkiaSharp;
using TechnicolorPatcher.Texture.Layers;
using TechnicolorPatcher.Types;
using TechnicolorPatcher.Util;
using TechnicolorPatcher.Util.Image;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace TechnicolorPatcher.Texture;

public class ConfigTexture
{
    public required string Name { get; init; }
    public required Int2 Size { get; init; }
    
    public Dictionary<string, SKBitmap> GroupOutput { get; } = [];
    public Dictionary<string, SKBitmap> FillImages { get; } = [];

    private Dictionary<string, List<LayerBase>> Groups { get; init; } = [];
    private Dictionary<string, SKBitmap> MaskImages { get; } = [];

    public void Apply(FileInfo outputFile, FileInfo maskFile)
    {
        Masks.Setup(maskFile, Size, FillImages, Groups, MaskImages);

        foreach (string groupName in Groups.Keys)
        {
            ApplyGroup(groupName);
        }
        
        FileInfo outputFileAlbedo = new(outputFile.FullName + "-a.png");
        FileInfo outputFileMetal  = new(outputFile.FullName + "-m.png");
        FileInfo outputFileTc     = new(outputFile.FullName + "-tc.png");
        
        SKBitmap albedoImage = GroupOutput["diffuse"].PasteAlpha(GroupOutput["gloss"]);
        SKBitmap metalImage = GroupOutput["metal"];
        SKBitmap tcImage = Channels.MergeChannels(
            GroupOutput["color_primary"], 
            GroupOutput["color_secondary"], 
            GroupOutput["gloss_alt"], 
            GroupOutput["metal_alt"]);

        Directory.CreateDirectory(outputFileAlbedo.DirectoryName!);
        albedoImage.SaveDds(outputFileAlbedo);
        metalImage.SaveDds(outputFileMetal);
        tcImage.SaveDds(outputFileTc);
        
        SaveLoad.ClearCache();
    }

    private void ApplyGroup(string groupName)
    {
        SKBitmap bitmap = new(Size.X, Size.Y, SKColorType.Rgba8888, SKAlphaType.Unpremul);

        for (int index = 0; index < Groups[groupName].Count; index++)
        {
            LayerBase layer = Groups[groupName][index];
            
            layer.Validate(this, index);
            bitmap = layer.Apply(bitmap, MaskImages[layer.MaskId]);
        }

        GroupOutput[groupName] = bitmap;
    }

    public static ConfigTexture FromYaml(string yaml, string name)
    {
        IDeserializer deserializer = new StaticDeserializerBuilder(new YamlStaticContextCustom())
            .WithNamingConvention(UnderscoredNamingConvention.Instance)
            .WithNodeDeserializer(new LayerBaseDeserializer())
            .WithNodeDeserializer(new Int2Deserializer())
            .Build();
        
        ConfigTextureYaml configTextureYaml = deserializer.Deserialize<ConfigTextureYaml>(yaml);
        ConfigTexture configTexture = new()
        {
            Name = name,
            Size = configTextureYaml.Size,
            Groups = new Dictionary<string, List<LayerBase>>
            {
                ["color_primary"] = configTextureYaml.ColorPrimary,
                ["color_secondary"] = configTextureYaml.ColorSecondary,
                ["diffuse"] = configTextureYaml.Diffuse,
                ["gloss"] = configTextureYaml.Gloss,
                ["gloss_alt"] = configTextureYaml.GlossAlt,
                ["metal"] = configTextureYaml.Metal,
                ["metal_alt"] = configTextureYaml.MetalAlt,
            }
        };
        
        return configTexture;
    }
}

[YamlSerializable]
public class ConfigTextureYaml
{
    public Int2 Size { get; set; } = new(0, 0);
    public List<LayerBase> ColorPrimary { get; set; } = [];
    public List<LayerBase> ColorSecondary { get; set; } = [];
    public List<LayerBase> Diffuse { get; set; } = [];
    public List<LayerBase> Gloss { get; set; } = [];
    public List<LayerBase> GlossAlt { get; set; } = [];
    public List<LayerBase> Metal { get; set; } = [];
    public List<LayerBase> MetalAlt { get; set; } = [];
}