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
        if (!Config.GroupOutput.ContainsKey(GroupName))
        {
            throw new ArgumentException("Group name is invalid, or has not run yet: " + GroupName);
        }
    }

    protected override SKBitmap GenerateLayer(SKBitmap groupBitmap)
    {
        SKBitmap layerBitmap = Config.GroupOutput[GroupName].Copy();

        return layerBitmap;
    }
}