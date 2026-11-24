using SkiaSharp;
using TechnicolorPatcher.Util.Image;
using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Texture.Layers;

[YamlSerializable]
public class LayerBase
{
    protected ConfigTexture Config { get; set; } = null!;

    [YamlMember(Alias = "masks")] 
    public string[] MaskNames { get; set; } = [];

    [YamlIgnore] 
    public string MaskId => string.Join(";", MaskNames); 
    
    [YamlIgnore] 
    public int LayerIndex { get; set; }

    public SKBitmap Apply(SKBitmap groupBitmap, SKBitmap maskBitmap)
    {
        SKBitmap layerBitmap = GenerateLayer(groupBitmap);
        SKBitmap layerClipped = layerBitmap.PasteAlpha(maskBitmap);
        SKBitmap result = groupBitmap.Overlay(layerClipped);
        return result;
    }

    protected virtual SKBitmap GenerateLayer(SKBitmap groupBitmap)
    {
        throw new NotSupportedException();
    }
    
    public void Validate(ConfigTexture config, int layerIndex)
    {
        Config = config;
        LayerIndex = layerIndex;
        
        Validate();
    }

    protected virtual void Validate()
    {
        throw new NotSupportedException();
    }
}