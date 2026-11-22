using TechnicolorPatcher.Util;

namespace TechnicolorPatcherTests;

public class ColorTests
{
    [Fact]
    public void TestHSV()
    {
        byte[] rgb1 = [117, 165, 135];
        float[] hsv = SkiaUtils.ToHSV(rgb1);
        Assert.True(hsv[0] - 142 < 1.0f);
        Assert.True(hsv[1] -  29 < 1.0f);
        Assert.True(hsv[2] -  64 < 1.0f);
        
        byte[] rgb2 = SkiaUtils.ToRGB(hsv);
        Assert.Equal(rgb1, rgb2);
    }
}