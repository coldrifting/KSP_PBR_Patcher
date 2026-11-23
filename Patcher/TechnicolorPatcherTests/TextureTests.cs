using SkiaSharp;
using TechnicolorPatcher.Util.Image;

namespace TechnicolorPatcherTests;

public class TextureTests
{
    [Fact]
    public void TestComposite()
    {
        SKImageInfo info = new(4, 4);
        
        SKBitmap input =  new(info);
        input.Erase(SKColors.Red);
        
        SKBitmap overlay = new(info);
        overlay.Erase(SKColors.Transparent);

        SKColor[]? p = overlay.Pixels;
        
        for (int i = 0; i < p.Length; i++)
        {
            if (i % 4 == 1)
            {
                p[i] = new SKColor(255, 255, 255, 255);
            }
            else
            {
                p[i] = new SKColor(0, 0, 0, 0);
            }
        }

        overlay.Pixels = p;
        
        SKBitmap output = input.Overlay(overlay);

        output.SavePng(new FileInfo(@"C:\Users\coldrifting\desktop\test.png"));
    }
}