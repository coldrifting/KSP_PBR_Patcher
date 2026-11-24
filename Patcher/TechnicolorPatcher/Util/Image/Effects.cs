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

            Dictionary<uint, uint> lookup = new();

            for (int y = 0; y < bitmapPointer.Height; y++) {
                uint* rowBase = bitmapPointer.GetRowBase(y);
                uint* rowResult = resultPointer.GetRowBase(y);

                for (int x = 0; x < bitmapPointer.Width; x++)
                {
                    uint pixel = rowBase[x];
                    byte a = (byte)((pixel >> 24) & 0xFF);

                    if (lookup.TryGetValue(pixel, out uint value))
                    {
                        rowResult[x] = (uint)(a << 24) | (value & 0x00FFFFFF);
                        continue;
                    }

                    byte b = (byte)(pixel & 0xFF);
                    byte g = (byte)((pixel >> 8) & 0xFF);
                    byte r = (byte)((pixel >> 16) & 0xFF);
                        
                    byte[] rgb = [r,g,b];
                    float[] hsv = Common.ToHsv(rgb);
                    hsv[1] = Math.Clamp(hsv[1] * percent, 0, 100.0f);
                    byte[] rgb2 = Common.ToRgb(hsv);
                        
                    uint rx = (uint)(255 << 24 | rgb2[0] << 16 | rgb2[1] << 8 | rgb2[2]);
                    lookup.Add(pixel, rx);
                    rowResult[x] = (uint)(a << 24) | (rx & 0x00FFFFFF);
                }
            }

            return result;
        }
    }
}