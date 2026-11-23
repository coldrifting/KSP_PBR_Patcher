using SkiaSharp;
using TechnicolorPatcher.Util;

namespace TechnicolorPatcherTests;

public class TextureTests
{
    [Fact]
    public void TestComposite()
    {
        var info = new SKImageInfo(4, 4);
        
        var input =  new SKBitmap(info);
        input.Erase(SKColors.Red);
        
        var overlay = new SKBitmap(info);
        overlay.Erase(SKColors.Transparent);

        var p = overlay.Pixels;
        
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
        
        input.Paste(overlay);

        input.SavePng(@"C:\Users\coldrifting\desktop\test.png");
    }
}