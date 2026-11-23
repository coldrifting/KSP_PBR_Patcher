using SkiaSharp;
using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Texture.Layers;

[YamlSerializable]
public class LayerCopy : LayerBase
{
    public static string LayerName => "copy";
    
    [YamlMember(Alias = "group")]
    public required string GroupName { get; set; }

    protected override void Validate()
    {
        if (!Config.Groups.ContainsKey(GroupName))
        {
            throw new ArgumentException("Invalid group name: " + GroupName);
        }
    }
    
    public override SKBitmap GenerateLayer(SKBitmap groupBitmap)
    {
        SKBitmap layerBitmap = Config.Groups[GroupName].Copy();

        return layerBitmap;
    }
}