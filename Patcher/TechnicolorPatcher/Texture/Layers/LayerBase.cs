using SkiaSharp;
using Svg;
using Svg.Skia;
using TechnicolorPatcher.Texture.Config;
using TechnicolorPatcher.Util.Image;
using YamlDotNet.Serialization;
using Color = System.Drawing.Color;

namespace TechnicolorPatcher.Texture.Layers;

[YamlSerializable]
public class LayerBase
{
    protected ConfigTexture Config { get; set; } = null!;

    [YamlMember(Alias = "masks")] 
    public List<string> MaskNames { get; set; } = [];
    
    protected SKBitmap Mask { get; set; } = new(4,4, SKColorType.Rgba8888, SKAlphaType.Premul);

    protected Dictionary<string, SKBitmap> FillImages { get; set; } = [];
    
    [YamlIgnore] 
    public int LayerIndex { get; set; }

    public void GenerateMask(FileInfo maskFile)
    {
        if (MaskNames.Count > 0 && !maskFile.Exists)
        {
            throw new ArgumentException("Masks specified, but no mask file was found");
        }
        
        // Generate Mask
        SvgDocument? svgDoc = SvgDocument.Open(maskFile.FullName);
        if (svgDoc is null)
        {
            throw new Exception("This shouldn't happen... :(");
        }

        svgDoc.Children.Insert(0, new SvgRectangle
        {
            ID = "bg",
            X = 0,
            Y = 0,
            Width = svgDoc.Width,
            Height = svgDoc.Height,
            Fill = new SvgColourServer
            {
                Colour = Color.Black
            }
        });
        
        Dictionary<string, bool> maskInfo = MaskNames
            .ToDictionary(s => s.EndsWith('!') ? s[..^1] : s, s => s.EndsWith('!'));
        
        foreach (SvgElement element in svgDoc.Children)
        {
            if (element.ID is null)
            {
                continue;
            }

            if (element is SvgImage svgImage)
            {
                if (svgImage.Href.StartsWith("data:image/png;base64,"))
                {
                    string? imageBase64 = svgImage.Href[22..^1];
                    Stream s = new MemoryStream(Convert.FromBase64String(imageBase64));
                    SKBitmap? embeddedImage = SKBitmap.Decode(s);
                    if (embeddedImage.AlphaType == SKAlphaType.Premul)
                    {
                        SKColor[]? pixels = embeddedImage.Pixels;

                        embeddedImage = new SKBitmap(embeddedImage.Width, embeddedImage.Height, embeddedImage.ColorType, SKAlphaType.Unpremul);
                        embeddedImage.Pixels = pixels;
                    }
                    if (embeddedImage is null)
                    {
                        throw new ArgumentException("An error occured while decoding a SVG embedded image");
                    }
                    
                    if (embeddedImage.ColorType == SKColorType.Rgba8888)
                    {
                        FillImages[element.ID] = embeddedImage;
                    }
                    else
                    {
                        FillImages[element.ID] = embeddedImage.Copy(SKColorType.Rgba8888);
                    }
                }
            }
            
            if (!maskInfo.TryGetValue(element.ID, out bool invert))
            {
                element.Display = "none";
                continue;
            }
            
            if (element is SvgVisualElement)
            {
                if (element is SvgImage)
                {
                    continue;
                }
                
                if (element.Fill is SvgColourServer colourServer)
                {
                    if (element.ID == "bg")
                    {
                        colourServer.Colour = invert ? Color.White : Color.Black;
                    }
                    else
                    {
                        colourServer.Colour = invert ? Color.Black : Color.White;
                    }
                }
            }
        }
        
        using SKSvg svg = new();
        SKPicture? picture = svg.FromSvgDocument(svgDoc);
        if (picture is null)
        {
            throw new ArgumentException("Svg loading went wrong...");
        }
        
        int width = (int)picture.CullRect.Width;
        int height = (int)picture.CullRect.Height;
        
        SKBitmap mask = new(width, height, SKColorType.Rgba8888, SKAlphaType.Unpremul);
        if (maskInfo.Count == 0)
        {
            mask.Erase(SKColors.White);
        }
        else
        {
            using SKCanvas canvas = new(mask);
            canvas.DrawPicture(picture);
            canvas.Flush();
        }
        
        Mask = mask;
    }

    public SKBitmap Apply(SKBitmap groupBitmap)
    {
        SKBitmap layerBitmap = GenerateLayer(groupBitmap);
        SKBitmap layerClipped = layerBitmap.PasteAlpha(Mask);
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

        if (MaskNames.Count == 0)
        {
            MaskNames.Insert(0, "bg!");
        }
        else if (!MaskNames[0].StartsWith("bg"))
        {
            MaskNames.Insert(0, "bg");
        }

        Validate();
    }

    protected virtual void Validate()
    {
        throw new NotSupportedException();
    }
}