using SkiaSharp;
using TechnicolorPatcher.Types;
using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Texture.Layers;

[YamlSerializable]
public class LayerCopy : LayerBase
{
    public static string LayerName => "copy";
    
    [YamlMember(Alias = "group")]
    public required string GroupName { get; set; }
    
    public required Dictionary<string, SKBitmap> Groups { get; set; } = new();

    public override SKBitmap GenerateLayer(SKBitmap groupBitmap)
    {
        SKBitmap layerBitmap = Groups[GroupName].Copy();

        return layerBitmap;
    }
}