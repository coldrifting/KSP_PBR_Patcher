using SkiaSharp;
using TechnicolorPatcher.Util;
using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Texture.Layers;

[YamlSerializable]
public class LayerSaturation : LayerBase
{
    public static string LayerName => "saturation";
    
    [YamlMember(Alias = "percent")]
    public required float PercentInput { get; set; }

    private float Percent { get; set; } = 1.0f;

    protected override void Validate()
    {
        Percent = PercentInput / 100.0f;
    }

    public override SKBitmap GenerateLayer(SKBitmap groupBitmap)
    {
        SKBitmap layer = groupBitmap.Copy();
        layer.AdjustSaturation(Percent);

        return layer;
    }
}