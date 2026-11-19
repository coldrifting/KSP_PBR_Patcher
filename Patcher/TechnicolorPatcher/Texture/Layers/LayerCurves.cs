using SkiaSharp;
using TechnicolorPatcher.Types;
using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Texture.Layers;

[YamlSerializable]
public class LayerCurves : LayerBase
{
    public static string LayerName => "curves";
    
    public List<Int2> Points { get; set; }

    public void Validate()
    {
        int[] xVals = Points.Select(p => p.X).ToArray();
        if (!xVals.SequenceEqual(xVals.OrderBy(v => v)))
        {
            throw new ArgumentException("Curve points must be ordered by the x axis");
        }
    }

    public override SKBitmap Apply(SKBitmap groupBitmap)
    {
        // TODO
        return groupBitmap;
    }
}