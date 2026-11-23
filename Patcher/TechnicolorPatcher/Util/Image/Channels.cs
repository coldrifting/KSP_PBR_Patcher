using SkiaSharp;

namespace TechnicolorPatcher.Util.Image;

public static class Channels
{
    extension(SKBitmap bitmap)
    {
        public unsafe SKBitmap GetAlpha()
        {
            Common.Validate(bitmap);
        
            SKBitmap result = new(bitmap.Width, bitmap.Height, SKColorType.Rgba8888, SKAlphaType.Unpremul);
        
            SKBitmapPointer bitmapPointer = new(bitmap);
            SKBitmapPointer resultPointer = new(result);

            Parallel.For(0L, bitmapPointer.Height, y =>
            {
                uint* rowBase = bitmapPointer.GetRowBase(y);
                uint* rowResult = resultPointer.GetRowBase(y);
            
                for (int x = 0; x < bitmapPointer.Width; x++)
                {
                    byte a = (byte)((rowBase[x] >> 24) & 0xFF);
                    rowResult[x] = (uint)(255 << 24 | a << 16 | a << 8 | a);
                }
            });
            return result;
        }

        public unsafe SKBitmap ClearAlpha()
        {
            Common.Validate(bitmap);
        
            SKBitmap result = new(bitmap.Width, bitmap.Height, SKColorType.Rgba8888, SKAlphaType.Unpremul);
            
            SKBitmapPointer bitmapPointer = new(bitmap);
            SKBitmapPointer resultPointer = new(result);
            
            Parallel.For(0L, bitmapPointer.Height, y =>
            {
                uint* rowBase = bitmapPointer.GetRowBase(y);
                uint* rowResult = resultPointer.GetRowBase(y);
            
                for (int x = 0; x < bitmapPointer.Width; x++)
                {
                    rowResult[x] = rowBase[x] | 0xFF000000;
                }
            });
            
            return result;
        }
        
        /// Assumes alpha comes from R channel of alpha bitmap, not A channel
        public unsafe SKBitmap PasteAlpha(SKBitmap alpha)
        {
            Common.Validate(bitmap, alpha);
            
            SKBitmap result = new(bitmap.Width, bitmap.Height, SKColorType.Rgba8888, SKAlphaType.Unpremul);
        
            SKBitmapPointer bitmapPointer = new(bitmap);
            SKBitmapPointer alphaPointer = new(alpha);
            SKBitmapPointer resultPointer = new(result);

            Parallel.For(0L, bitmapPointer.Height, y =>
            {
                uint* rowBase = bitmapPointer.GetRowBase(y);
                uint* rowAlpha = alphaPointer.GetRowBase(y);
                uint* rowResult = resultPointer.GetRowBase(y);
            
                for (int x = 0; x < bitmapPointer.Width; x++)
                {
                    uint c = rowBase[x] & 0x00FFFFFF;
                    uint a = (rowAlpha[x] & 0x000000FF) << 24;
                    
                    rowResult[x] = c | a;
                }
            });
            
            return result;
        }
        
        // Assumes BG is fully opaque
        public unsafe SKBitmap Overlay(SKBitmap overlay)
        {
            Common.Validate(bitmap, overlay);
            
            SKBitmap result = new(bitmap.Width, bitmap.Height, SKColorType.Rgba8888, SKAlphaType.Unpremul);

            SKBitmapPointer bitmapPointer = new(bitmap);
            SKBitmapPointer overlayPointer = new(overlay);
            SKBitmapPointer resultPointer = new(result);
        
            Parallel.For(0L, bitmapPointer.Height, y =>
            {
                // Calculate exact start of the row using RowBytes
                uint* rowBase = bitmapPointer.GetRowBase(y);
                uint* rowOverlay = overlayPointer.GetRowBase(y);
                uint* rowResult = resultPointer.GetRowBase(y);

                for (int x = 0; x < bitmapPointer.Width; x++)
                {
                    byte rBg = (byte)((rowBase[x] >> 0) & 0xFF);
                    byte gBg = (byte)((rowBase[x] >> 8) & 0xFF);
                    byte bBg = (byte)((rowBase[x] >> 16) & 0xFF);

                    byte rFg = (byte)((rowOverlay[x] >> 0) & 0xFF);
                    byte gFg = (byte)((rowOverlay[x] >> 8) & 0xFF);
                    byte bFg = (byte)((rowOverlay[x] >> 16) & 0xFF);
                    byte aFg = (byte)((rowOverlay[x] >> 24) & 0xFF);

                    const byte aOut = 255;
                    byte rOut = (byte)((aFg * rFg + (255 - aFg) * rBg) / 255);
                    byte gOut = (byte)((aFg * gFg + (255 - aFg) * gBg) / 255);
                    byte bOut = (byte)((aFg * bFg + (255 - aFg) * bBg) / 255);

                    rowResult[x] = (uint)(aOut << 24 | bOut << 16 | gOut << 8 | rOut);
                }
            });

            return result;
        }
    }
        
    /// Assumes alpha comes from R channel of alpha bitmap, not A channel
    public static unsafe SKBitmap MergeChannels(SKBitmap red, SKBitmap green, SKBitmap blue, SKBitmap alpha)
    {
        Common.Validate(red, green, blue, alpha);
            
        SKBitmap result = new(red.Width, red.Height, SKColorType.Rgba8888, SKAlphaType.Unpremul);
        
        SKBitmapPointer redPointer = new(red);
        SKBitmapPointer greenPointer = new(green);
        SKBitmapPointer bluePointer = new(blue);
        SKBitmapPointer alphaPointer = new(alpha);
        
        SKBitmapPointer resultPointer = new(result);
        
        Parallel.For(0L, redPointer.Height, y =>
        {
            uint* redBase   = redPointer.GetRowBase(y);
            uint* greenBase = greenPointer.GetRowBase(y);
            uint* blueBase  = bluePointer.GetRowBase(y);
            uint* alphaBase = alphaPointer.GetRowBase(y);
            
            uint* resultBase = resultPointer.GetRowBase(y);
            
            for (int x = 0; x < red.Width; x++)
            {
                uint r = redBase[x]   & 0x000000FF;
                uint g = greenBase[x] & 0x0000FF00;
                uint b = blueBase[x]  & 0x00FF0000;
                uint a = (alphaBase[x] & 0x000000FF) << 24;
                    
                resultBase[x] = a | b | g | r;
            }
        });

        return result;
    }
}