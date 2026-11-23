using System.Diagnostics;
using SkiaSharp;
using TechnicolorPatcher.Texture.Layers;
using TechnicolorPatcher.Types;
using TechnicolorPatcher.Util;
using TechnicolorPatcher.Util.Image;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace TechnicolorPatcher.Texture.Config;

[YamlSerializable]
public class ConfigTexture
{
    public required string Name { get; set; }
    public required Int2 Size { get; set; }

    public required List<LayerBase> ColorPrimary { get; set; }
    public required List<LayerBase> ColorSecondary { get; set; }
    public required List<LayerBase> Diffuse { get; set; }
    public required List<LayerBase> Gloss { get; set; }
    public required List<LayerBase> GlossAlt { get; set; }
    public required List<LayerBase> Metal { get; set; }
    public required List<LayerBase> MetalAlt { get; set; }

    public Dictionary<string, SKBitmap> Groups { get; } = new();

    public void Apply(FileInfo outputFile, FileInfo maskFile)
    {
        Groups["color_primary"]   = ApplyGroup(ColorPrimary, maskFile);
        Groups["color_secondary"] = ApplyGroup(ColorSecondary, maskFile);
        Groups["diffuse"]         = ApplyGroup(Diffuse, maskFile);
        Groups["gloss"]           = ApplyGroup(Gloss, maskFile);
        Groups["gloss_alt"]       = ApplyGroup(GlossAlt, maskFile);
        Groups["metal"]           = ApplyGroup(Metal, maskFile);
        Groups["metal_alt"]       = ApplyGroup(MetalAlt, maskFile);
        
        FileInfo outputFileAlbedo = new(outputFile.FullName + "-a.png");
        FileInfo outputFileMetal  = new(outputFile.FullName + "-m.png");
        FileInfo outputFileTc     = new(outputFile.FullName + "-tc.png");
        
        SKBitmap albedoImage = Groups["diffuse"].PasteAlpha(Groups["gloss"]);
        SKBitmap metalImage = Groups["metal"];
        SKBitmap tcImage = Channels.MergeChannels(Groups["color_primary"], Groups["color_secondary"], Groups["gloss_alt"], Groups["metal_alt"]);

        Directory.CreateDirectory(outputFileAlbedo.DirectoryName!);
        albedoImage.SaveDds(outputFileAlbedo);
        metalImage.SaveDds(outputFileMetal);
        tcImage.SaveDds(outputFileTc);
        
        SaveLoad.ClearCache();
    }

    private SKBitmap ApplyGroup(List<LayerBase> layers, FileInfo maskFile)
    {
        SKBitmap bitmap = new(Size.X, Size.Y, SKColorType.Rgba8888, SKAlphaType.Unpremul);

        for (int index = 0; index < layers.Count; index++)
        {
            LayerBase layer = layers[index];
            
            layer.Validate(this, index);
            layer.GenerateMask(maskFile);
            bitmap = layer.Apply(bitmap);
        }
        
        return bitmap;
    }

    public static ConfigTexture FromYaml(string yaml)
    {
        IDeserializer deserializer = new StaticDeserializerBuilder(new YamlStaticContextCustom())
            .WithNamingConvention(UnderscoredNamingConvention.Instance)
            .WithNodeDeserializer(new LayerBaseDeserializer())
            .WithNodeDeserializer(new Int2Deserializer())
            .Build();
        
        ConfigTexture configTexture = deserializer.Deserialize<ConfigTexture>(yaml);

        return configTexture;
    }
}