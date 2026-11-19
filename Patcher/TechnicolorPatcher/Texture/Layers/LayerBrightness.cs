using SkiaSharp;
using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Texture.Layers;

[YamlSerializable]
public class LayerBrightness : LayerBase
{
    public static string LayerName => "brightness";
    
    public required float Percent { get; set; }

    public override SKBitmap Apply(SKBitmap groupBitmap)
    {
        // TODO
        return groupBitmap;
    }
}