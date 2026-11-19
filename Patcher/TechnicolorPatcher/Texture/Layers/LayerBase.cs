using SkiaSharp;
using Svg;
using Svg.Skia;
using TechnicolorPatcher.Types;
using TechnicolorPatcher.Util;
using YamlDotNet.Serialization;
using Color = System.Drawing.Color;

namespace TechnicolorPatcher.Texture.Layers;

[YamlSerializable]
public class LayerBase
{
    [YamlIgnore]
    public Int2 Size { get; set; }

    [YamlMember(Alias = "masks")] 
    public List<string> MaskNames { get; set; } = [];

    [YamlIgnore] 
    public string GroupType { get; set; } = "";

    [YamlIgnore] 
    public Dictionary<string, SKBitmap> FillImages { get; set; } = [];
    
    [YamlIgnore] 
    public SKBitmap? Mask { get; set; }

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

    public virtual SKBitmap Apply(SKBitmap groupBitmap)
    {
        throw new NotSupportedException();
    }

    public SKBitmap ApplyLayerMask(SKBitmap groupBitmap, SKBitmap layerBitmap, bool ignoreMask = false)
    {
        if (Mask is null)
        {
            var x = new SKBitmap(groupBitmap.Width, groupBitmap.Height, SKColorType.Rgba8888, SKAlphaType.Opaque);
            x.Erase(SKColors.Red);
            return x;
        }

        SKBitmap result;
        if (ignoreMask)
        {
            result = groupBitmap.Paste(layerBitmap);
        }
        else
        {
            // Clip layer image to mask
            SKBitmap layerClipped = SkiaUtils.MergeBitmaps(layerBitmap, Mask);
        
            // Paste over current group image
            result = groupBitmap.Paste(layerClipped);
        }
        
        return result;
    }
}