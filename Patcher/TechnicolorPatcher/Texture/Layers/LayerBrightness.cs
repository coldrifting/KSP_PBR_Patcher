using SkiaSharp;
using TechnicolorPatcher.Util;
using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Texture.Layers;

[YamlSerializable]
public class LayerBrightness : LayerBase
{
    public static string LayerName => "brightness";
    
    public required float Percent { get; set; }

    public override SKBitmap GenerateLayer(SKBitmap groupBitmap)
    {
        SKColor[]? pixels = groupBitmap.Pixels;

        for (int i = 0; i < pixels.Length; i++)
        {
            byte r = (byte)Math.Clamp(Math.Abs(pixels[i].Red * Percent), 0, 255);
            byte g = (byte)Math.Clamp(Math.Abs(pixels[i].Green * Percent), 0, 255);
            byte b = (byte)Math.Clamp(Math.Abs(pixels[i].Blue * Percent), 0, 255);
            pixels[i] = new SKColor(r, g, b, pixels[i].Alpha);
        }
        
        SKBitmap layer = new(groupBitmap.Info);
        layer.Pixels = pixels;

        SKBitmap output = groupBitmap.Paste(layer);
        
        return ApplyLayerMask(groupBitmap, output);
    }
}