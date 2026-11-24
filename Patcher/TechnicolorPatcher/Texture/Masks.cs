using System.Drawing;
using SkiaSharp;
using Svg;
using Svg.Skia;
using TechnicolorPatcher.Texture.Layers;
using TechnicolorPatcher.Types;

namespace TechnicolorPatcher.Texture;

public static class Masks
{
    public static void Setup(FileInfo maskFile, Int2 size, Dictionary<string, SKBitmap> fillImages, Dictionary<string, List<LayerBase>> layerGroups, Dictionary<string, SKBitmap> maskImages)
    {
        SvgDocument svgDoc;
        if (!maskFile.Exists)
        {
            svgDoc = new SvgDocument
            {
                Width = size.X,
                Height = size.Y,
                ViewBox = new SvgViewBox(0, 0, size.X, size.Y)
            };
        }
        else
        {
            svgDoc = SvgDocument.Open(maskFile.FullName);
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

        foreach (SvgElement element in svgDoc.Children)
        {
            if (element.ID is not null && element is SvgImage svgImage)
            {
                if (svgImage.Href.StartsWith("data:image/png;base64,"))
                {
                    string? imageBase64 = svgImage.Href[22..^1];
                    Stream s = new MemoryStream(Convert.FromBase64String(imageBase64));
                    SKBitmap? embeddedImage = SKBitmap.Decode(s);
                    if (embeddedImage.AlphaType == SKAlphaType.Premul)
                    {
                        SKColor[]? pixels = embeddedImage.Pixels;

                        embeddedImage = new SKBitmap(embeddedImage.Width, embeddedImage.Height, embeddedImage.ColorType,
                            SKAlphaType.Unpremul);
                        embeddedImage.Pixels = pixels;
                    }

                    if (embeddedImage is null)
                    {
                        throw new ArgumentException("An error occured while decoding a SVG embedded image");
                    }

                    if (embeddedImage.ColorType == SKColorType.Rgba8888)
                    {
                        fillImages[element.ID] = embeddedImage;
                    }
                    else
                    {
                        fillImages[element.ID] = embeddedImage.Copy(SKColorType.Rgba8888);
                    }
                }
            }
        }

        Dictionary<string, (string, bool)[]> identifiers = new();
        foreach (List<LayerBase> layers in layerGroups.Values)
        {
            foreach (LayerBase layer in layers)
            {
                if (layer.MaskNames.Length == 0)
                {
                    layer.MaskNames = ["bg!"];
                }
                else if (!layer.MaskNames[0].StartsWith("bg"))
                {
                    layer.MaskNames = ["bg", ..layer.MaskNames];
                }
                
                (string, bool)[] names = layer.MaskNames
                    .Select(name => name.EndsWith('!') 
                        ? (name[..^1], true) 
                        : (name, false)).ToArray();
                identifiers[layer.MaskId] = names;
            }
        }

        foreach ((string key, (string, bool)[] names) in identifiers)
        {
            // Setup SVG
            string[] namesArr = names.Select(s => s.Item1).ToArray();
            foreach (SvgElement element in svgDoc.Children)
            {
                if (element is SvgVisualElement && element.ID is not null)
                {
                    int index = namesArr.IndexOf(element.ID);
                    if (index != -1)
                    {
                        element.Display = "block";
                        
                        if (element.Fill is SvgColourServer colourServerFill)
                        {
                            if (element.ID == "bg")
                            {
                                
                                colourServerFill.Colour = names[index].Item2 ? Color.White : Color.Black;
                            }
                            else
                            {
                                colourServerFill.Colour = names[index].Item2 ? Color.Black : Color.White;
                            }
                        }
                        
                        if (element.Stroke is SvgColourServer colourServerStroke)
                        {
                            colourServerStroke.Colour = names[index].Item2 ? Color.Black : Color.White;
                        }
                    }
                    else
                    {
                        element.Display = "none";
                    }
                }
            }
            
            // Save Mask as bitmap
            using SKSvg svg = new();
            SKPicture? picture = svg.FromSvgDocument(svgDoc);
            if (picture is null)
            {
                throw new ArgumentException("Svg loading went wrong...");
            }
        
            int width = (int)picture.CullRect.Width;
            int height = (int)picture.CullRect.Height;
        
            SKBitmap mask = new(width, height, SKColorType.Rgba8888, SKAlphaType.Unpremul);
            using SKCanvas canvas = new(mask);
            canvas.DrawPicture(picture);
            canvas.Flush();
            
            maskImages[key] = mask;
        }
    }
}