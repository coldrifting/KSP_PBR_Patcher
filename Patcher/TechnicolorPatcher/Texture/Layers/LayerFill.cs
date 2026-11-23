using SkiaSharp;
using TechnicolorPatcher.Util;
using TechnicolorPatcher.Util.Image;
using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Texture.Layers;

[YamlSerializable]
public class LayerFill : LayerBase
{
    public static string LayerName => "fill";
    
    [YamlMember(Alias = "color")]
    public string? ColorInput  { get; set; }
    
    [YamlIgnore]
    public SKColor? Color { get; set; }
    
    public string? Image { get; set; }
    public string? Channels { get; set; }
    public float? Scale { get; set; }

    protected override void Validate()
    {
        if (Image is null && ColorInput is null)
        {
            throw new ArgumentException("Missing required value image or color");
        }

        if (Image is not null && Color is not null)
        {
            throw new ArgumentException("Only image or color values can be specified, not both");
        }

        if (ColorInput is not null)
        {
            if (SKColor.TryParse(ColorInput, out SKColor colorHex))
            {
                Color = colorHex;
            }
            else
            {
                Color = ColorInput.ToLower() switch
                {
                    "gray" or "grey" => SKColors.Gray,
                    "white" => SKColors.White,
                    "black" => SKColors.Black,
                    "red" => SKColors.Red,
                    "green" => SKColors.Green,
                    "blue" => SKColors.Blue,
                    "cyan" => SKColors.Cyan,
                    "purple" => SKColors.Purple,
                    "yellow" => SKColors.Yellow,
                    "magenta" => SKColors.Magenta,
                    _ => throw new NotSupportedException($"Invalid named color: {ColorInput}")
                };
            }
        }
        
        Channels ??= "RGBA";
        Scale ??= 1;
    }

    protected override SKBitmap GenerateLayer(SKBitmap groupBitmap)
    {
        SKBitmap layerBitmap;
        if (Color is not null)
        {
            layerBitmap = new SKBitmap(groupBitmap.Width, groupBitmap.Height, groupBitmap.ColorType, SKAlphaType.Unpremul);
            layerBitmap.Erase(Color.Value);
        }
        else if (Image is not null)
        {
            if (Image.Contains('/') || Image.Contains('\\'))
            {
                FileInfo imageSource = new(Path.Combine(Patcher.GameDataPath!.FullName, Image));
                if (!imageSource.Exists)
                {
                    throw new ArgumentException($"The file does not exist: \n{imageSource.FullName}");
                }

                layerBitmap = SaveLoad.LoadDds(imageSource.FullName);
                layerBitmap = Channels?.ToLower() switch
                {
                    "a"   => layerBitmap.GetAlpha(),
                    "rgb" => layerBitmap.ClearAlpha(),
                    _     => layerBitmap
                };
            }
            else
            {
                layerBitmap = FillImages[Image].Copy();
                Mask = layerBitmap.GetAlpha();
            }
        }
        else
        {
            throw new NotSupportedException("This should not happen");
        }

        return layerBitmap;
    }
}