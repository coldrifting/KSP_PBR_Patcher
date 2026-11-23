using SkiaSharp;

namespace TechnicolorPatcher.Util.Image;

public static class Effects
{
    extension(SKBitmap bitmap)
    {
        public unsafe SKBitmap AdjustBrightness(float percent)
        {
            ArgumentOutOfRangeException.ThrowIfGreaterThan(percent, 2.0f);

            Common.Validate(bitmap);
            
            SKBitmap result = new(bitmap.Width, bitmap.Height, SKColorType.Rgba8888, SKAlphaType.Unpremul);
        
            SKBitmapPointer bitmapPointer = new(bitmap);
            SKBitmapPointer resultPointer = new(result);
        
            byte[] lut = new byte[256];
            for (int i = 0; i < 256; i++)
            {
                lut[i] = (byte)Math.Clamp(Math.Floor(i * percent), 0, 255);
            }

            Parallel.For(0L, bitmapPointer.Height, y =>
            {
                uint* rowBase = bitmapPointer.GetRowBase(y);
                uint* rowResult = resultPointer.GetRowBase(y);

                for (int x = 0; x < bitmapPointer.Width; x++)
                {
                    uint pixel = rowBase[x];
                    byte r = (byte)((pixel >> 0) & 0xFF);
                    byte g = (byte)((pixel >> 8) & 0xFF);
                    byte b = (byte)((pixel >> 16) & 0xFF);
                    byte a = (byte)((pixel >> 24) & 0xFF);
                
                    rowResult[x] = (uint)((a << 24) | (lut[b] << 16) | (lut[g] << 8) | lut[r]);
                }
            });

            return result;
        }

        public unsafe SKBitmap AdjustSaturation(float percent)
        {
            ArgumentOutOfRangeException.ThrowIfGreaterThan(percent, 2.0f);

            Common.Validate(bitmap);
            
            SKBitmap result = new(bitmap.Width, bitmap.Height, SKColorType.Rgba8888, SKAlphaType.Unpremul);
        
            SKBitmapPointer bitmapPointer = new(bitmap);
            SKBitmapPointer resultPointer = new(result);

            uint[,,] lut = new uint[256,256,256];
            for (int r = 0; r < 256; r++)
            {
                for (int g = 0; g < 256; g++)
                {
                    for (int b = 0; b < 256; b++)
                    {
                        byte[] rgb = [(byte)r,(byte)g,(byte)b];
                        float[] hsv = Common.ToHsv(rgb);
                        hsv[1] = Math.Clamp(hsv[1] * percent, 0, 100.0f);
                        byte[] rgb2 = Common.ToRgb(hsv);
                        lut[r, g, b] = (uint)(255 << 24 | rgb2[0] << 16 | rgb2[1] << 8 | rgb2[2]);
                    }
                }
            }

            Parallel.For(0L, bitmapPointer.Height, y =>
            {
                uint* rowBase = bitmapPointer.GetRowBase(y);
                uint* rowResult = resultPointer.GetRowBase(y);

                for (int x = 0; x < bitmapPointer.Width; x++)
                {
                    uint pixel = rowBase[x];
                    byte b = (byte)(pixel & 0xFF);
                    byte g = (byte)((pixel >> 8) & 0xFF);
                    byte r = (byte)((pixel >> 16) & 0xFF);
                    byte a = (byte)((pixel >> 24) & 0xFF);
                    // Direct pointer read/write with zero bounds checks
                
                    uint rgbNew = lut[r, g, b];

                    rowResult[x] = ((uint)a << 24) | rgbNew;
                }
            });

            return result;
        }
    }
}