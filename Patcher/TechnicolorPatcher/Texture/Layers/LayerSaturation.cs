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

    [YamlIgnore]
    public float Percent { get; set; } = 1.0f;

    public void Validate()
    {
        Percent = PercentInput / 100.0f;
    }

    public override SKBitmap GenerateLayer(SKBitmap groupBitmap)
    {
        SKColor[]? pixels = groupBitmap.Pixels;
        
        for (int i = 0; i < pixels.Length; i++)
        {
            byte[] rgb = [pixels[i].Red, pixels[i].Green, pixels[i].Blue];
            float[] hsv = SkiaUtils.ToHSV(rgb);
            hsv[1] = Math.Clamp(hsv[1] * Percent, 0, 100.0f);
            byte[] rgb2 = SkiaUtils.ToRGB(hsv);
            
            pixels[i] = new SKColor(rgb2[0], rgb2[1], rgb2[2], pixels[i].Alpha);
        }
        
        SKBitmap layer = new(groupBitmap.Info);
        layer.Pixels = pixels;

        SKBitmap output = groupBitmap.Paste(layer);
        
        return ApplyLayerMask(groupBitmap, output);
    }
}